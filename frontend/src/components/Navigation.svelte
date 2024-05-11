<script>
    import { link } from 'svelte-spa-router'
    import { page, keyword, access_token, username, is_login } from '../lib/store' // 로그인 정보 표시
</script>

<!-- 네비게이션바 -->
<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
    <div class="container-fluid">
        <!-- 로고 누르면 페이지, 검색어 정보 초기화 -->
        <a use:link class="navbar-brand" href="/" on:click="{() => {$keyword = '', $page = 0}}">Hihi</a>
        <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon" />
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <!-- 로그인 여부에 따라 표시 -->
                {#if $is_login }
                    <li class="nav-item">
                        <!-- 로그아웃 클릭 시 스토어 변수 초기화 -->
                        <a use:link href="/user-login" class="nav-link" on:click={() => {
                            $access_token = ''
                            $username = ''
                            $is_login = false
                        }}>로그아웃 ({$username})</a>
                    </li>
                {:else}
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/user-create">회원가입</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/user-login">로그인</a>
                    </li>
                {/if}
            </ul>
        </div>
    </div>
</nav>
