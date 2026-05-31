# Trouble Lab

AWS 기반 장애 대응 훈련 플랫폼

## 프로젝트 개요

실제 운영 환경에서 발생할 수 있는 장애를 의도적으로 재현하고, 로그 분석과 복구 과정을 학습하기 위한 프로젝트입니다.

### 아키텍처

```text
Client
 ↓
API Gateway
 ↓
Lambda
 ↓
DynamoDB
```

### 기술 스택

* AWS Lambda
* API Gateway
* DynamoDB
* CloudWatch Logs
* IAM
* Terraform
* Python

---

## 구현 기능

### GET /health

서비스 상태 확인 API

응답 예시

```json
{
  "status": "ok",
  "service": "trouble-lab"
}
```

### GET /users

DynamoDB 사용자 목록 조회 API

응답 예시

```json
{
  "users": [
    {
      "user_id": "user-001",
      "name": "kang",
      "role": "admin"
    }
  ]
}
```

---

# 장애 대응 시나리오 01

## 장애 내용

Lambda 실행 Role에서 DynamoDB 조회 권한을 제거하여 사용자 조회 API 장애를 재현

### 변경 전

```text
Lambda
 └─ dynamodb:Scan 허용
```

### 변경 후

```text
Lambda
 └─ dynamodb:Scan 제거
```

---

## 장애 증상

API 호출 결과

```http
GET /users

500 Internal Server Error
```

사용자는 사용자 목록을 조회할 수 없는 상태가 됨.

---

## 원인 분석

CloudWatch Logs 확인

```text
AccessDeniedException

not authorized to perform:
dynamodb:Scan
```

오류 메시지를 통해 Lambda 실행 Role에 DynamoDB Scan 권한이 존재하지 않음을 확인.

---

## 조치 내용

Terraform IAM Policy 복구

```hcl
Action = [
  "dynamodb:Scan",
  "dynamodb:GetItem"
]
```

Terraform Apply 수행

```bash
terraform apply
```

---

## 결과

API 정상 복구

```json
{
  "users": [
    {
      "user_id": "user-001",
      "name": "kang",
      "role": "admin"
    }
  ]
}
```

---

## 학습 내용

* IAM 정책 변경이 서비스 동작에 미치는 영향 확인
* CloudWatch Logs 기반 장애 원인 분석 경험
* Terraform을 통한 인프라 복구 경험
* 최소 권한 원칙(Least Privilege) 이해
* 서버리스 환경에서의 운영 및 장애 대응 경험

```
```
