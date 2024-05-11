import qs from "qs"
import { access_token, username, is_login } from "./store"
import { get } from 'svelte/store'
import { push } from 'svelte-spa-router'

// operation : 데이터 처리 방법
// url : 요청 url. 백엔드 서버 호스트명 이후의 url만 전달
// params : 요청 데이터
const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation
    let content_type = 'application/json'
    let body = JSON.stringify(params)

    // 로그인 api 요청
    // OAuth2 사용한 로그인 api 요청 시 헤더 항목 중 Content-Type을 application/x-www-form-urlencoded로 사용해야 함
    // 일반적으로 fastapi가 post 요청 시 Content-Type: application/json
    if(operation === 'login') {
        method = 'post'
        content_type = 'application/x-www-form-urlencoded'
        body = qs.stringify(params) // params 데이터를 'application/x-www-form-urlencoded' 형식에 맞게끔 변환
    }
    
    // 등록한 환경변수 불러오기
    let _url = import.meta.env.VITE_SERVER_URL+url
    if(method === 'get') { // 요청이 get인 경우 파라미터를 get 방식에 맞게 URLSearchParams 사용해 파라미터 조립
        _url += "?" + new URLSearchParams(params)
    }

    let options = {
        method: method,
        headers: {
            "Content-Type": content_type
        }
    }

    // http 헤더에 액세스 토큰 담아 호출
    const _access_token = get(access_token)
    if (_access_token) {
        options.headers["Authorization"] = "Bearer " + _access_token
    }

    if (method !== 'get') { // 요청이 get이 아닌 경우 options['body']에 전달받은 파라미터 값 설정
        options['body'] = body // body 항목에 값 설정할 때는 params를 json 문자열로 변경해야 함
    }

    fetch(_url, options)
        .then(response => {
            // 응답 상태코드가 204인 경우 응답 결과가 없어도 success_callback 실시
            if(response.status === 204) {  // No content
                if(success_callback) {
                    success_callback() // 응답 결과 없으므로 파라미터 없이 함수만 호출
                }
                return
            }

            response.json()
                .then(json => {
                    if(response.status >= 200 && response.status < 300) {  // 200 ~ 299
                        if(success_callback) { // 호출한 api의 리턴값을 입력으로 전달해 호출
                            success_callback(json)
                        }
                    // 질문 등록 시 글쓴이 정보 저장
                    }else if(operation !== 'login' && response.status === 401) { // token time out or operation이 login이 아닌데 401 오류가 발생할 경우
                        // 사용자 정보 초기화
                        access_token.set('') // 스토어 변수의 값 읽으려면 get, 저장할 때는 set
                        username.set('')
                        is_login.set(false)
                        alert("로그인이 필요합니다.") 
                        push('/user-login')
                    }else {
                        if (failure_callback) { // 오류값이 입력값으로 주어짐
                            failure_callback(json)
                        }else {
                            alert(JSON.stringify(json))
                        }
                    }
                })
                .catch(error => {
                    alert(JSON.stringify(error))
                })
        })
}

export default fastapi
