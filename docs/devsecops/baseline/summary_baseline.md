## Resumen de seguridad

| Herramienta | CRITICAL | HIGH | MEDIUM | LOW | INFO | Total |
|---|---:|---:|---:|---:|---:|---:|
| Bandit | 0 | 0 | 2 | 10 | 0 | 12 |
| Checkov | 0 | 0 | 3 | 0 | 0 | 3 |
| Gitleaks | 0 | 46 | 0 | 0 | 0 | 46 |
| Semgrep | 0 | 1 | 20 | 0 | 431 | 452 |
| Trivy | 0 | 0 | 0 | 3 | 0 | 3 |
| npm audit | 12 | 85 | 80 | 14 | 0 | 191 |
| pip-audit | 0 | 0 | 1 | 0 | 0 | 1 |
| **Total** | **12** | **132** | **106** | **27** | **431** | **708** |

### Hallazgos CRITICAL / HIGH

| Severidad | Herramienta | Regla | Hallazgo | Ubicación |
|---|---|---|---|---|
| CRITICAL | npm audit | GHSA-fjxv-7rqg-78g4 | form-data: form-data uses unsafe random function in form-data for choosing boundary | npm-audit-frontend |
| CRITICAL | npm audit | GHSA-2w6w-674q-4c4q | handlebars: Handlebars.js has JavaScript Injection via AST Type Confusion | npm-audit-frontend |
| CRITICAL | npm audit | GHSA-8r5x-fm3f-whwj | handlebars: Handlebars: JavaScript Injection via AST Type Confusion in compile (bypass of CVE-2026-33937) | npm-audit-frontend |
| CRITICAL | npm audit | GHSA-p8wg-vrv2-v86f | handlebars: Handlebars: JavaScript Injection via Own Property Check Bypass | npm-audit-frontend |
| CRITICAL | npm audit | GHSA-9qr9-h5gf-34mp | next: Next.js is vulnerable to RCE in React flight protocol | npm-audit-frontend |
| CRITICAL | npm audit | GHSA-p293-qw3h-jr36 | next: Next.js: Unauthenticated Remote Code Execution on windows-hosted servers | npm-audit-frontend |
| CRITICAL | npm audit | GHSA-2xp9-vwfh-vxw4 | next: Next.js: Unauthenticated Remote Code Execution in Image Optimization API when AVIF files are used | npm-audit-frontend |
| CRITICAL | npm audit | GHSA-2464-fhr4-w9xw | next: Next.js: Unauthenticated Remote Code Execution in Image Optimization API when SVG files are used | npm-audit-frontend |
| CRITICAL | npm audit | GHSA-xq3m-2v4x-88gg | protobufjs: protobufjs has an arbitrary code execution issue | npm-audit-frontend |
| CRITICAL | npm audit | GHSA-jqcg-44mw-7w3h | proxy-addr: proxy-addr vulnerable to IP spoofing via IPv4-mapped IPv6 trust subnet | npm-audit-frontend |
| CRITICAL | npm audit | GHSA-xv26-6w52-cph6 | websocket-driver: websocket-driver: Message corruption via abuse of protocol length headers | npm-audit-frontend |
| CRITICAL | npm audit | GHSA-jqcg-44mw-7w3h | proxy-addr: proxy-addr vulnerable to IP spoofing via IPv4-mapped IPv6 trust subnet | npm-audit-ms-classroom |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/02-Student/01-student-me.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/02-Student/03-student-submit-quiz.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/02-Student/02-student-modify.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/02-Student/04-student-quiz-list.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/02-teacher-modify.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/06-teacher-competence.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/05-teacher-competence.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/08-teacher-classroom-quiz-create.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/08-teacher-classroom-quiz-create.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/07-teacher-classroom-competence-associate.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/09-teacher-generate-quiz-from-pdf.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/09-teacher-generate-quiz-from-pdf.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/01-classroom-all-student.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/01-classroom-all-student.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/02-classroom-all-teacher.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/02-classroom-all-teacher.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/05-classroom-competences.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/05-classroom-competences.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/04-classroom-by-id.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/04-classroom-by-id.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/06-classroom-ranking.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/05-Quiz/01-quiz-by-id.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/06-classroom-competence-ranking.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/05-Quiz/03-quiz-list.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/05-Quiz/02-quiz-student-result.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/05-Quiz/Create New Quiz.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/05-Quiz/20-quiz-create-full.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/01-Auth/04-auth-validate-token-role.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/01-Auth/03-auth-validate-token.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/02-Student/04-student-add-coins.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/02-Student/03-student-ids-by-email.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/02-Student/05-student-buy-character.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/03-Teacher/02-teacher-by-id.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/03-Teacher/03-teacher-ids-by-email.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/01-teacher-me.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/01-teacher-me.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/04-teacher-classroom-add-users.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/04-teacher-classroom-add-users.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/03-teacher-create-classroom.bru:19 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/03-teacher-create-classroom.bru:21 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/10-teacher-generate-quiz-from-text.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/03-classroom-by-user-id.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/03-classroom-by-user-id.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/02-Student/02-student-by-id.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/02-Student/01-student-me.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/03-Teacher/01-teacher-me.bru:14 |
| HIGH | npm audit | GHSA-5375-pq7m-f5r2 | @grpc/grpc-js: @grpc/grpc-js: A malformed request can cause a server crash | npm-audit-frontend |
| HIGH | npm audit | GHSA-99f4-grh7-6pcq | @grpc/grpc-js: @grpc/grpc-js: An incoming malformed compressed message can cause a client or server crash | npm-audit-frontend |
