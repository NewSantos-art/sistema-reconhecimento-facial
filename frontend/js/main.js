function verificarLogin() {
    const paginaAtual = window.location.pathname
    const ehLogin = paginaAtual.includes('login.html')
    const logado = sessionStorage.getItem('logado')

    if (!logado && !ehLogin) {
        window.location.href = 'login.html'
    }
}

verificarLogin()

const API = 'http://127.0.0.1:5000'

function irPara(pagina) {
    window.location.href = pagina
}