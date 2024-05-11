<script> 
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import { page, keyword, is_login } from '../lib/store'
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko') // 한국 날짜 형식으로 표시

    let question_list = [] // 초깃값이 없을 경우 fetch 함수가 비동기 방식으로 실행됨
    // 페이징
    let size = 10
    let total = 0
    let kw = '' // 검색 키워드
    $: total_page = Math.ceil(total/size) // 전체 페이지 개수 != 게시물 총 건수(total)
    // 반응형 변수 : total 변수가 api 호출로 인해 값이 변하면 total_page 변수도 재계산됨

    // fastapi 함수 사용
    // 필요한 부분 스토어 변수 적용
    function get_question_list(_page) { // 질문목록 api 호출하는 함수 // 결괏값을 question_list에 대입
        let params = {
            page: $page, // 페이지 번호 입력해 질문 목록 api 호출하기 위해
            size: size,
            keyword: $keyword, // 스토어 변수
        }
        
        fastapi('get', '/api/question/list', params, (json) => { // 화살표 함수 - success_callback : 응답받은 json 데이터를 question_list에 대입
            // ailure_callback 함수 전달하지 않더라도 fastapi 함수는 오류 발생시 오류의 내용을 alert로 표시
            question_list = json.question_list // 질문 목록 api 출력 항목이 딕셔너리로 바뀌어서 => 한 페이지에 10건만 출력
            total = json.total
            kw = $keyword
        }) 
    }

    // 스토어 변수를 반응형 변수로 설정
    // $: 반응형 기호 => page, keyword 값이 변경되면 get_question_list 함수 다시 호출
    $:$page, $keyword, get_question_list()
</script>

<!-- 질문 목록 부트스트랩 -->
<div class="container my-3">
  <!-- 검색 기능 -->
  <div class="row my-3">
    <div class="col-6">
        <a use:link href="/question-create" 
            class="btn btn-primary {$is_login ? '' : 'disabled'}">질문 등록하기</a>
    </div>
    <div class="col-6">
        <div class="input-group">
            <input type="text" class="form-control" bind:value="{kw}">
            <!-- 입력값을 $keyword에 저장해 get_question_list 함수 자동 실행, $page = 0 : 검색 결과는 항상 첫 페이지부터 -->
            <button class="btn btn-outline-secondary" on:click={() => {$keyword = kw, $page = 0}}>
                찾기
            </button>
        </div>
    </div>
  </div>

  <table class="table">
      <thead>
      <tr class="text-center table-dark">
          <th>번호</th>
          <th style="width:50%">제목</th>
          <th>글쓴이</th>
          <th>작성일시</th>
      </tr>
      </thead>
      <tbody>
      {#each question_list as question, i}
      <tr class="text-center">
          <!-- 게시물 일련번호 표시 -->
          <td>{ total - ($page * size) - i }</td>
          <td class="text-start">
                <!-- use:link : url에 항상 /# 문자가 선행되게 경로가 생성됨 => 해당 경로를 하나의 페이지로 인식 => 해시 기반 라우팅 -->
              <a use:link href="/detail/{question.id}">{question.subject}</a>
              <!-- 답변 개수 표시 -->
              {#if question.answers.length > 0 }
              <span class="text-danger small mx-2">{question.answers.length}</span>
              {/if}
          </td>
          <!-- 글쓴이 표시. 값이 없으면 빈 값 표시 -->
          <td>{ question.user ? question.user.username : "" }</td>
          <td>{moment(question.create_date).format('YYYY년 MM월 DD일 hh:mm a')}</td>
      </tr>
      {/each}
      </tbody>
  </table>
  <!-- 페이징 -->
    <ul class="pagination justify-content-center">
        <!-- 이전페이지 -->
        <!-- page가 0보다 작거나 같으면 disabled(비활성화) 속성 적용 -->
        <li class="page-item {$page <= 0 && 'disabled'}">
            <button class="page-link" on:click="{() => $page--}">이전</button>
        </li>
        <!-- 페이지번호 -->
        {#each Array(total_page) as _, loop_page}
        <!-- 페이지 표시 제한 -->
        {#if loop_page >= $page-5 && loop_page <= $page+5} 
        <!-- 루프로 반복되는 페이지 번호가 현재 페이지 번호와 같을 경우 active 클래스 적용해(활성화) 강조 -->
        <li class="page-item {loop_page === $page && 'active'}">
            <button on:click="{() => $page = loop_page}" class="page-link">{loop_page+1}</button>
        </li>
        {/if}
        {/each}
        <!-- 다음페이지 -->
        <!-- 다음 페이지 없으면 비활성화 -->
        <li class="page-item {$page >= total_page-1 && 'disabled'}">
            <button class="page-link" on:click="{() => $page++}">다음</button>
        </li>
    </ul>
</div>