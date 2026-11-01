# Spring 결재 롤백과 오류 로그 보존 검토

확인일: 2026-11-01. 아래는 Spring의 일반적인 동기식 프록시 트랜잭션을 기준으로 한 참고 설계이며, 과거 회사 구현을 복원한 코드가 아니다. 실제 사용한 Spring 버전, XML/AOP·어노테이션 설정, 호출 경계와 로그 저장 코드는 별도 확인이 필요하다. 공개 포트폴리오에는 이미 확인된 ‘업무와 오류 로그 트랜잭션 분리’ 설명만 유지한다.

## 핵심 결론

`try` 블록 자체에는 트랜잭션 경계가 없다. 업무 DB 변경을 하나의 트랜잭션에 묶어 실패하면 롤백하고, 오류 로그 INSERT를 독립 트랜잭션에서 커밋해야 한다. 오류 로그는 DB 테이블에 저장하는 경우를 전제로 한다. SLF4J로 파일이나 콘솔에 출력하는 로그는 보통 DB 트랜잭션 롤백 대상이 아니다.

## 권장 예시: 업무 트랜잭션이 종료된 뒤 catch에서 로그 기록

세 클래스는 각각 별도의 Spring Bean이다. 생성자 주입과 저장소 구현은 생략한 구조 예시다. `@Transactional`은 `org.springframework.transaction.annotation.Transactional`을 사용한다. 여기서 REQUIRES_NEW는 결재 한 건과 로그 각각의 물리 트랜잭션을 분리하기 위한 선택이며, 당시 `requirednew=true`가 정확히 같은 구현이었는지는 미확인이다.

```java
// Bean 1: 호출 흐름 조정. 예시에서는 이 메서드를 감싸는 외부 트랜잭션 없음.
@Service
public class ApprovalFacade {
    // 생성자로 주입: approvalTxService, failureLogService
    public void processOne(Long approvalId) throws Exception {
        try {
            approvalTxService.approve(approvalId);
        } catch (Exception businessFailure) {
            // approve의 프록시가 트랜잭션을 롤백한 뒤 이 catch에 도달
            try {
                failureLogService.save(approvalId, businessFailure);
            } catch (Exception logFailure) {
                businessFailure.addSuppressed(logFailure);
                // 실제 운영에서는 로그 저장 실패를 별도 로깅·알림 경로로 전달
            }
            throw businessFailure; // 원래 결재 실패를 호출자에게 전달
        }
    }
}

// Bean 2: 실패 시 되돌릴 DB 변경을 이 경계 안에서 수행
@Service
public class ApprovalTxService {
    @Transactional(
        propagation = Propagation.REQUIRES_NEW,
        rollbackFor = Exception.class
    )
    public void approve(Long approvalId) throws Exception {
        approvalProcessor.preprocess(approvalId);
        approvalRepository.complete(approvalId);
        // 예외를 여기서 삼키지 않고 프록시 밖으로 전달
    }
}

// Bean 3: 결재 트랜잭션과 독립적으로 로그 커밋
@Service
public class FailureLogService {
    @Transactional(
        propagation = Propagation.REQUIRES_NEW,
        rollbackFor = Exception.class
    )
    public void save(Long approvalId, Exception failure) {
        failureLogRepository.insert(approvalId, failure.getMessage());
    }
}
```

호출 순서: Facade → 결재 프록시 → 결재 트랜잭션 시작 → 업무 예외 → 프록시 롤백 → Facade catch → 로그 프록시 → 로그 트랜잭션 시작·커밋 → 원래 예외 전달.

전처리·완료 갱신이 같은 트랜잭션 매니저가 관리하는 DB 자원을 사용한다는 전제다. 전처리 내부에서 별도 트랜잭션을 커밋하거나 외부 API·파일·메시지 전송을 수행했다면, 그 효과까지 위 DB 롤백으로 취소되는 것은 아니다. 시작 단계에서 이미 커밋한 ‘처리중’ 상태도 건별 트랜잭션 롤백으로 되돌아가지 않는다.

Facade에 어노테이션이 없다는 사실만으로 호출 스택에 외부 트랜잭션이 없다고 단정할 수는 없다. 예시는 외부 트랜잭션 없이 호출하는 구조다. 상위에서 트랜잭션이 전달되더라도 두 REQUIRES_NEW는 독립 트랜잭션을 사용하지만, 바깥 자원을 유지하면서 추가 연결을 얻을 수 있으므로 풀 크기와 잠금 경합을 검토해야 한다.

## 같은 트랜잭션 안의 try/catch를 유지하는 경우

```java
// 이 메서드도 다른 Bean에서 프록시를 통해 호출되어야 함
@Transactional(rollbackFor = Exception.class)
public void processOne(Long approvalId) throws Exception {
    try {
        approvalProcessor.preprocess(approvalId);
        approvalRepository.complete(approvalId);
    } catch (Exception failure) {
        failureLogService.save(approvalId, failure); // 별도 Bean, REQUIRES_NEW
        throw failure; // 메서드 프록시가 업무 트랜잭션을 롤백
    }
}
```

이 구조에서는 로그가 커밋된 뒤 바깥 업무 트랜잭션이 롤백된다. 로그 저장까지 기본 REQUIRED로 묶으면 업무 롤백에 로그도 포함될 수 있다. 반대로 로그만 REQUIRES_NEW로 바꾸고 업무 예외를 삼키면, 업무 쪽 롤백은 자동 보장되지 않는다. 위 구조는 업무 트랜잭션이 잠금을 잡은 동안 로그를 저장하므로, 로그 INSERT가 같은 행·미커밋 데이터에 의존하지 않도록 검토한다.

예외를 다시 던지지 않고 실패 결과를 반환해야 하는 경우에는 활성 트랜잭션 안에서 `TransactionAspectSupport.currentTransactionStatus().setRollbackOnly()` 등으로 롤백 의사를 명시할 수 있다. 다만 상위 REQUIRED 트랜잭션에 참여 중이면 전체 롤백과 UnexpectedRollbackException으로 이어질 수 있다. 부분 작업만 되돌리는 기능으로 해석하면 안 된다.

프로그램 방식이었던 경우에는 `TransactionTemplate.execute(...)`의 경계 안에서 예외를 던지거나, 콜백의 `status.setRollbackOnly()`를 호출하는 형태였을 수 있다. 이것은 당시 구현에 대한 가능한 단서이며 사용 사실을 확정한 설명은 아니다.

## 구현을 확인할 때 볼 지점

- 예외 포착 위치: 결재 트랜잭션 안인가, 결재 프록시 호출이 끝난 바깥인가?
- 롤백 규칙: 기본값은 RuntimeException·Error, checked Exception은 `rollbackFor` 또는 별도 설정 확인. `rollbackFor=Exception.class`도 예외를 catch에서 삼키면 그 사실만으로 작동하지 않는다.
- 호출 방식: 기본 프록시 모드에서 `this.saveLog()` 같은 자기 호출은 별도 메서드의 REQUIRES_NEW 설정을 새로 적용하지 않는다. 별도 Bean을 주입받아 호출하거나 명시적인 프로그램 트랜잭션 경계가 필요하다.
- 전파 차이: REQUIRES_NEW는 독립 물리 트랜잭션. NESTED는 일반적으로 같은 물리 트랜잭션의 세이브포인트이므로 업무 전체 롤백 후 로그 보존 용도로 같게 취급할 수 없다.
- 로그 저장 성공의 의미: 업무 롤백과 독립적인 커밋을 구성할 수 있다는 뜻이다. DB 장애·제약 위반·연결 실패까지 배제하는 절대적 저장 보장은 아니다. 로그 실패가 원래 업무 예외를 덮지 않도록 처리한다.

## 검증한다면 필요한 최소 시나리오

업무 DB 변경 직후 런타임 예외와 checked 예외를 각각 발생시키고, 호출 완료 후 새 트랜잭션/새 연결에서 업무 데이터가 롤백되고 실패 로그가 남는지 확인한다. 실패 로그 저장 자체가 실패하는 경우와 실제 스케줄러·비동기 진입 경로에서도 확인한다. 테스트 자체를 한 트랜잭션으로 묶어 결과를 가리지 않는다. 이 문서는 구현 원리 분석이며 실제 프로젝트 코드에 대한 통합 테스트를 실행한 결과가 아니다.

## 기록 문구

현재 확인 가능한 표현:

> 결재 실패 시 업무 데이터가 롤백되더라도 오류 이력을 남길 수 있도록, 업무 처리와 오류 로그 저장의 트랜잭션 경계를 분리했습니다.

과거 코드를 확인한 후 실제 일치할 때만 추가할 표현:

> 결재 처리 예외가 트랜잭션 경계를 벗어나도록 구성하고, 오류 로그는 별도 서비스의 REQUIRES_NEW 트랜잭션에서 저장했습니다.

## 공식 근거

- [롤백 규칙과 예외 전달](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/rolling-back.html)
- [REQUIRED·REQUIRES_NEW·NESTED와 자원 사용](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/tx-propagation.html)
- [프록시와 자기 호출](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html)
- [TransactionTemplate과 setRollbackOnly](https://docs.spring.io/spring-framework/reference/data-access/transaction/programmatic.html)
