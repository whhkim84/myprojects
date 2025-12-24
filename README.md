# 간단한 웹스캐너 탐지기 (honeypot)

간단한 Flask 기반 웹 애플리케이션으로 웹 스캐너(크롤러/스캐닝 도구)를 탐지합니다.

파일
- `repo/scanner_detector/app.py` - Flask 앱 엔트리포인트
- `repo/scanner_detector/detector.py` - 탐지 로직
- `repo/requirements.txt` - 의존성
- `repo/test_scripts/test_scanner.py` - 간단한 테스트 스크립트 (옵션)

실행 방법 (Windows 예시)

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python repo/scanner_detector/app.py
```

리눅스/macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python repo/scanner_detector/app.py
```

테스트
- 브라우저로 `http://localhost:8000/` 접속: 정상(200) 응답
- User-Agent를 `sqlmap` 등으로 바꾸거나 빠른 요청을 여러 경로로 보내면 403 및 탐지 로그가 `detections.log`에 기록됩니다.

간단한 테스트 스크립트 사용

```bash
python repo/test_scripts/test_scanner.py
```

주의
- 이 코드는 교육/연구 목적의 간단한 탐지 예시입니다. 실환경에서 사용하려면 더 정교한 시그니처, 지속 저장소, 보안 고려가 필요합니다.
