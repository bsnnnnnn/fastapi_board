<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"

    let error = {detail:[]}
    let subject = ''
    let content = ''

    function post_question(event) {
        event.preventDefault()
        let url = "/api/question/create"
        let params = {
            subject: subject,
            content: content,
        }
        fastapi('post', url, params, 
            (json) => { // 질문 등록 성공하면 질문 목록 화면으로 이동 // success_callback 함수 중 push 함수 사용
                push("/") // app.svelte에 등록된 라우터 중 / 경로에 해당하는 화면(=질문 목록 화면)으로 이동
            },
            (json_error) => {
                error = json_error
            }
        )
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">질문 등록</h5>
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="subject">제목</label>
            <input type="text" class="form-control" bind:value="{subject}">
        </div>
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value="{content}"></textarea>
        </div>
        <!-- post_question 함수 실행 -->
        <button class="btn btn-primary" on:click="{post_question}">저장하기</button>
    </form>
</div>