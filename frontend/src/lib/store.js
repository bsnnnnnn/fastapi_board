import { writable } from 'svelte/store'

// 스토어 변수 생성
// key, initValue 입력받아 writable 스토어 생성해 리턴
const persist_storage = (key, initValue) => {
    const storedValueStr = localStorage.getItem(key) // localStorage 사용해 지속성 가짐
    // 저장 시 json.stringify, 읽을 때 json.parse 사용 => localstorage에 저장하는 값을 항상 문자열로 유지
    const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)
    store.subscribe((val) => { // 스토어에 저장된 값이 변경될 때 실행되는 콜백 함수
        localStorage.setItem(key, JSON.stringify(val)) // 스토어 값이 변경되면 localstorage 값도 함께 변경됨
    })
    return store
}

export const page = persist_storage("page", 0)
export const keyword = persist_storage("keyword", "") // 검색 키워드
// 로그인 정보 - 지속성 스토어(새로고침해도 유지되어야 함)
export const access_token = persist_storage("access_token", "")
export const username = persist_storage("username", "")
export const is_login = persist_storage("is_login", false) // 로그인 여부 체크. api 응답값 아니지만 로그인 성공하면 true로