# Syncn!
**Sticy Note**를 사용하면서 icloud의 동기화가 부러웠던 적이 있으세요?? **Syncn**을 써보세요!!

*	언제 어디서나 기록한 메모를 볼 수 있습니다. 매번 동기화를 하지 않아도 됩니다!!
* 기존에 사용하던 이메일로 로그인 하세요. 따로 회원가입이 필요 없습니다.
* 더 이상 번거로운 프로그램을 사용하지 마세요. 간편한 “SyncN”으로 Sticky Note를 100% 활용해보세요


## 목차
 [1. 사용법](https://github.com/Fhwang0926/syncn_v1/blob/master/README.MD#%EC%82%AC%EC%9A%A9%EB%B2%95)  
 [2. 구조]  
 [3. 발전가능성]  
 [4. 설치 환경] (실행환경 언급해도 좋을듯)(rabbitmq 설치법 & 쉘스크립트, exe빌드 사용법, 사용된 라이브러리 등등)  
 [5. 문제점 & 버그]  
 [6. 시연 동영상]  



## 사용법
### 1. 설치
**Syncn**은 별도 웹페이지에 설치 파일을 제공하고 있습니다.

* 아래 첨부된 파일을 다운받으세요 & 아래 링크를 클릭하세요
* 프로그램을 다운 받아주세요 (기본 설치 경로는 ProgramFile 입니다)

url입력칸 & exe파일 첨부 칸



### 2. 인증
**Syncn**은 여러분이 가지고 있는 이메일을 통해 인증이 가능합니다. 입력창에 이메일을 입력하면 인증 URL이 메일로 발송됩니다. 그리고 그 링크를 클릭하기만 하면 인증이 완료됩니다. 인증이 끝나면 서버와 연결할 수 있는 설정파일(Setting.syncn)이 생겨요!

* 설치된 **Syncn**을 실행합니다.
* 입력창에 여러분의 Email을 입력해주세요 ex) abc@gmail.com
* 입력한 이메일의 수신함을 확인해주세요.
* 받은 메일안의 URL을 클릭해주세요.(※이메일을 입력 후 3분안에 클릭해야 합니다.)
* "Auth Successfully"라는 팝업창이 뜹니다. 확인을 눌러주세요
* **Syncn**프로그램으로 돌아가 "OK"버튼을 눌러주세요.

<img src="https://github.com/Fhwang0926/syncn_v1/blob/master/Image/EmailWrite.gif" width="30%"></img> 
<img src="https://github.com/Fhwang0926/syncn_v1/blob/master/Image/EmailAuth.gif" width="60%" height="400"></img>


### 3. 동기화
[인증](https://github.com/Fhwang0926/syncn_v1/new/master) 절차가 끝났다면 여러분은 평상시처럼 **Sticy Note**를 이용하면 됩니다. **Syncn**은 백그라운드에서 자동으로 실행됩니다. 만약 동기화를 멈추고 싶다면 트레이 아이콘에서 설정할 수 있어요.

* 동기화를 원하는 컴퓨터에도 **Syncn** 프로그램이 [설치](http://www.test.com)해 주세요. 
* **Syncn**을 처음 설치하는 컴퓨터일 경우 Email[인증](https://github.com/Fhwang0926/syncn_v1/new/master) 절차를 진행해 주셔야 합니다.
* **Syncn**이 설치되어 있고 Email[인증](https://github.com/Fhwang0926/syncn_v1/new/master)이 끝난 PC라면 이전과 같이 **Sticy Note**를 사용하시면 됩니다~

트레이 아이콘 동기화 옵션 gif파일 첨부 칸



## 
