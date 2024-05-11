<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte" 
    import { access_token, username, is_login } from "../lib/store" // 로그인 성공 시 스토어 변수

    let error = {detail:[]}
    let login_username = "" // 사용자 이름. 로그인 성공 시 username 항목을 리턴받음 -> 스토어 변수 username에 저장해 사용
    let login_password = ""

    function login(event) {
        event.preventDefault()
        let url = "/api/user/login"
        let params = {
            username: login_username,
            password: login_password,
        }
        fastapi('login', url, params, // operation 값으로 post 대신 login 전달
            (json) => {
                // 로그인 성공 시 스토어 변수에 저장
                $access_token = json.access_token
                $username = json.username
                $is_login = true
                push("/")
            },
            (json_error) => {
                error = json_error
            }
        )
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">로그인</h5>
    <Error error={error} />
    <form method="post">
        <div class="mb-3">
            <label for="username">사용자 이름</label>
            <input type="text" class="form-control" id="username" bind:value="{login_username}">
        </div>
        <div class="mb-3">
            <label for="password">비밀번호</label>
            <input type="password" class="form-control" id="password" bind:value="{login_password}">
        </div>
        <button type="submit" class="btn btn-primary" on:click="{login}">로그인</button>
    </form>
</div>
