<!-- <script>
  // let message; // 변수 선언. 서버에서 받아올 데이터 저장

  // // fetch : /hello 엔드포인트에 get 요청 보냄
  // fetch("http://127.0.0.1:8000/hello").then((response) => { // fetch 함수가 반환한 promise 객체의 then 메서드르 사용해 비동기적으로 서버의 응답 처리. 응답 객체를 response 매개변수로 전달
  //   response.json().then((json) => { // 응답을 json 형식으로 파싱, 파싱된 데이터를 json 매개변수로 전달
  //     message = json.message; // 파싱된 json 데이터에서 message 속성 값을 js 변수 message에 할당
  //   });
  // });
</script> -->

<!-- 링크 및 라우터 등록 -->
<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Detail from "./routes/Detail.svelte"
  import QuestionCreate from "./routes/QuestionCreate.svelte"
  import Navigation from "./components/Navigation.svelte"
  import UserCreate from "./routes/UserCreate.svelte"
  import UserLogin from "./routes/UserLogin.svelte"
  import QuestionModify from "./routes/QuestionModify.svelte"
  import AnswerModify from "./routes/AnswerModify.svelte"

  const routes = {
    '/': Home,
    // detail 뒤의 가변적인 값을 컴포넌트에 전달하기 위해 url 규칙 정의 필요
    '/detail/:question_id': Detail, // 요청된 detail 컴포넌트를 question_id로 읽을 수 있음
    '/question-create': QuestionCreate,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/question-modify/:question_id': QuestionModify,
    '/answer-modify/:answer_id': AnswerModify,
  }
</script>

<Navigation />
<!-- 주소에 매핑되는 컴포넌트 -->
<Router {routes}/>
