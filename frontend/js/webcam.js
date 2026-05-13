let stream = null

async function iniciarCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true })
        document.getElementById('video').srcObject = stream
    } catch(erro) {
        alert('Erro ao acessar a câmera: ' + erro.message)
    }
}

function pararCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop())
        stream = null
        document.getElementById('video').srcObject = null
    }
}

async function capturarEReconhecer() {
    const video = document.getElementById('video')
    const canvas = document.getElementById('canvas')
    const modalConteudo = document.getElementById('modalConteudo')
    const modal = new bootstrap.Modal(document.getElementById('modalResultado'))

    if (!stream) {
        alert('Inicie a câmera primeiro!')
        return
    }

    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    canvas.getContext('2d').drawImage(video, 0, 0)

    modalConteudo.innerHTML = '<p class="text-center">⏳ Analisando... aguarde.</p>'
    modal.show()

    canvas.toBlob(async (blob) => {
        try {
            const formData = new FormData()
            formData.append('imagem', blob, 'webcam.jpg')
            formData.append('metodo', 'webcam')

            const resposta = await fetch(`${API}/reconhecer`, {
                method: 'POST',
                body: formData
            })

            const dados = await resposta.json()

            if (dados.error) {
                modalConteudo.innerHTML = `<div class="alert alert-danger">${dados.error}</div>`
                return
            }

            if (dados.resultado === 'Pessoa identificada') {
                const html = `
                    <div class="alert alert-success">
                        <h5>✅ Pessoa Identificada!</h5>
                        <p><strong>Nome:</strong> ${dados.nome}</p>
                        <p><strong>ID:</strong> ${dados.id}</p>
                        <p><strong>Confiança:</strong> ${dados.confianca}</p>
                    </div>
                `
                modalConteudo.innerHTML = html
                document.getElementById('resultado').innerHTML = html
            } else {
                const html = '<div class="alert alert-warning">⚠️ Pessoa não identificada.</div>'
                modalConteudo.innerHTML = html
                document.getElementById('resultado').innerHTML = html
            }

        } catch(erro) {
            modalConteudo.innerHTML = `<div class="alert alert-danger">Erro: ${erro.message}</div>`
        }
    }, 'image/jpeg')
}