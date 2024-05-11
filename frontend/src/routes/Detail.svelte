<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { link, push } from 'svelte-spa-router'
    import { is_login, username } from "../lib/store"
    import { marked } from "marked"
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')

    export let params = {} // 컴포넌트 호출 시 전달한 파라미터 값 읽기 위해 변수 선언 필요
    let question_id = params.question_id
    // console.log('question_id:'+ question_id) // 전달된 파라미터
    let question = {answers:[], voter:[], content: ''} // 변수 1건에 대한 상세 정보이므로 초기화
    // question 변수의 content 항목 초기화하지 않으면 데이터 조회 전 화면 로드 시 marked.parse(quesiton.content)가 실행되어 undefined가 전달되어 오류가 발생
    let content = ""
    let error = {detail:[]}

    // 질문 상세 api 호출
    function get_question() {
        fastapi("get", "/api/question/detail/" + question_id, {}, (json) => {
            question = json // 출력값 저장
        })
    }

    get_question()

    // 답변 등록 api 호출
    function post_answer(event) {
        event.preventDefault() // submit 버튼이 눌릴 경우 form이 자동으로 전송되는 것 방지
        let url = "/api/answer/create/" + question_id
        let params = {
            content: content
        }
        fastapi('post', url, params, 
            (json) => {
                content = '' // 답변 등록이 성공하면 답변이 textarea에서 지워짐
                error = {detail:[]} // 에러 초깃값 
                get_question() // 상세 화면에 새로운 결괏값 반영
            },
            (err_json) => {
                error = err_json // 오류 내용 저장
            }
        )
    }

    // 질문 삭제
    function delete_question(_question_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/question/delete"
            let params = {
                question_id: _question_id
            }
            fastapi('delete', url, params, 
                (json) => {
                    push('/')
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

    // 답변 삭제
    function delete_answer(answer_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/answer/delete"
            let params = {
                answer_id: answer_id
            }
            fastapi('delete', url, params, 
                (json) => {
                    get_question()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

    // 질문 추천
    function vote_question(_question_id) {
        if(window.confirm('정말로 추천하시겠습니까?')) {
            let url = "/api/question/vote"
            let params = {
                question_id: _question_id
            }
            fastapi('post', url, params, 
                (json) => {
                    get_question()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

    // 답변 추천
    function vote_answer(answer_id) {
        if(window.confirm('정말로 추천하시겠습니까?')) {
            let url = "/api/answer/vote"
            let params = {
                answer_id: answer_id
            }
            fastapi('post', url, params, 
                (json) => {
                    get_question()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }
</script>

<div class="container my-3">
    <!-- 질문 -->
    <h2 class="border-bottom py-2">{question.subject}</h2>
    <div class="card my-3">
        <div class="card-body">
            <!-- 마크다운 적용 -->
            <div class="card-text">{@html marked.parse(question.content)}</div>
            <div class="d-flex justify-content-end">
                <!-- 수정 일시 -->
                {#if question.modify_date }
                <div class="badge bg-light text-dark p-2 text-start mx-3">
                    <div class="mb-2">modified at</div>
                    <div>{moment(question.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start">
                    <!-- 글쓴이 표시 -->
                    <div class="mb-2">{ question.user ? question.user.username : ""}</div>
                    <div>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
                <div class="my-3">
                    <!-- 질문 추천 -->
                    <button class="btn btn-sm btn-outline-secondary" on:click="{vote_question(question.id)}"> 
                        추천
                        <span class="badge rounded-pill bg-success">{ question.voter.length }</span>
                    </button>
                    <!-- 로그인한 사용자와 글쓴이가 같은 경우에만 작용 -->
                    {#if question.user && $username === question.user.username }
                    <!-- 질문 아이디 전달 -> 질문 데이터 불러오기 -->
                    <!-- 질문 수정 -->
                    <a use:link href="/question-modify/{question.id}" 
                        class="btn btn-sm btn-outline-secondary">수정</a>
                        <!-- 질문 삭제 -->
                        <button class="btn btn-sm btn-outline-secondary"
                            on:click={() => delete_question(question.id)}>삭제</button>
                    {/if}
                </div>
            </div>
        </div>
    </div>
    <!-- 질문 목록으로 -->
    <button class="btn btn-secondary" on:click="{() => {
        push('/')
    }}">목록으로</button>

    <!-- 답변 목록 -->
    <h5 class="border-bottom my-3 py-2">{question.answers.length}개의 답변이 있습니다.</h5>
    {#each question.answers as answer}
    <div class="card my-3">
        <div class="card-body">
            <!-- 마크다운 적용 -->
            <div class="card-text">{@html marked.parse(answer.content)}</div>
            <div class="d-flex justify-content-end">
                <!-- 답변 수정 일시 -->
                {#if answer.modify_date }
                <div class="badge bg-light text-dark p-2 text-start mx-3">
                    <div class="mb-2">modified at</div>
                    <div>{moment(answer.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{ answer.user ? answer.user.username : ""}</div>
                    <div>{moment(answer.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
                
                <div class="my-3">
                    <!-- 답변 추천 -->
                    <button class="btn btn-sm btn-outline-secondary" on:click="{vote_answer(answer.id)}"> 
                        추천
                        <span class="badge rounded-pill bg-success">{ answer.voter.length }</span>
                    </button>
                    <!-- 로그인한 사용자와 글쓴이가 같은 경우에만 보임 -->
                    {#if answer.user && $username === answer.user.username }
                    <!-- 답변 수정 -->
                    <a use:link href="/answer-modify/{answer.id}" 
                        class="btn btn-sm btn-outline-secondary">수정</a>
                    <!-- 답변 삭제 -->
                    <button class="btn btn-sm btn-outline-secondary"
                    on:click={() => delete_answer(answer.id) }>삭제</button>
                    {/if}
                </div>
            </div>
        </div>
    </div>
    {/each}
    <!-- 답변 등록 -->
    <!-- 에러 컴포넌트 -->
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <textarea rows="10" bind:value={content} disabled={$is_login ? "" : "disabled"} class="form-control" />
        </div>
        <!-- post answer 함수 호출 -> textarea에 작성한 content를 파라미터로 답변 등록 api 호출 -->
        <input type="submit" value="답변 등록" class="btn btn-primary {$is_login ? '' : 'disabled'}" on:click="{post_answer}" />
    </form>
</div>