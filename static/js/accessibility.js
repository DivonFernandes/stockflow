document.addEventListener("DOMContentLoaded", function() {
    // Referências aos elementos
    const btnAccessibility = document.getElementById('btn-accessibility');
    const panelAccessibility = document.getElementById('panel-accessibility');

    // Botões de opções
    const btnFonteGrande = document.getElementById('btn-fonte-grande');
    const btnDislexia = document.getElementById('btn-dislexia');
    const btnContraste = document.getElementById('btn-contraste');
    const btnSemAnimacao = document.getElementById('btn-sem-animacao');
    const btnLeitorTela = document.getElementById('btn-leitor-tela');

    // Estado inicial lido do localStorage
    let configs = {
        fonteGrande: localStorage.getItem('acc-fonte-grande') === 'true',
        dislexia: localStorage.getItem('acc-dislexia') === 'true',
        contraste: localStorage.getItem('acc-contraste') === 'true',
        semAnimacao: localStorage.getItem('acc-sem-animacao') === 'true',
        leitorTela: localStorage.getItem('acc-leitor-tela') === 'true'
    };

    // Função para aplicar as classes no body
    function applyConfigurations() {
        // Fonte Grande
        if (configs.fonteGrande) {
            document.body.classList.add('fonte-grande');
            if(btnFonteGrande) btnFonteGrande.classList.add('ativo');
        } else {
            document.body.classList.remove('fonte-grande');
            if(btnFonteGrande) btnFonteGrande.classList.remove('ativo');
        }

        // Dislexia
        if (configs.dislexia) {
            document.body.classList.add('fonte-dislexia');
            if(btnDislexia) btnDislexia.classList.add('ativo');
        } else {
            document.body.classList.remove('fonte-dislexia');
            if(btnDislexia) btnDislexia.classList.remove('ativo');
        }

        // Alto Contraste
        if (configs.contraste) {
            document.body.classList.add('alto-contraste');
            if(btnContraste) btnContraste.classList.add('ativo');
        } else {
            document.body.classList.remove('alto-contraste');
            if(btnContraste) btnContraste.classList.remove('ativo');
        }

        // Sem Animação
        if (configs.semAnimacao) {
            document.body.classList.add('sem-animacao');
            if(btnSemAnimacao) btnSemAnimacao.classList.add('ativo');
        } else {
            document.body.classList.remove('sem-animacao');
            if(btnSemAnimacao) btnSemAnimacao.classList.remove('ativo');
        }

        // Leitor de Tela
        if (configs.leitorTela) {
            if(btnLeitorTela) btnLeitorTela.classList.add('ativo');
        } else {
            if(btnLeitorTela) btnLeitorTela.classList.remove('ativo');
            if ('speechSynthesis' in window && window.speechSynthesis) {
                window.speechSynthesis.cancel();
            }
        }
    }

    // Aplica as configs assim que carrega
    applyConfigurations();

    // Toggle do painel
    if (btnAccessibility && panelAccessibility) {
        btnAccessibility.addEventListener('click', () => {
            panelAccessibility.classList.toggle('active');
        });
    }

    // Ações dos botões
    if (btnFonteGrande) {
        btnFonteGrande.addEventListener('click', () => {
            configs.fonteGrande = !configs.fonteGrande;
            localStorage.setItem('acc-fonte-grande', configs.fonteGrande);
            applyConfigurations();
        });
    }

    if (btnDislexia) {
        btnDislexia.addEventListener('click', () => {
            configs.dislexia = !configs.dislexia;
            localStorage.setItem('acc-dislexia', configs.dislexia);
            applyConfigurations();
        });
    }

    if (btnContraste) {
        btnContraste.addEventListener('click', () => {
            configs.contraste = !configs.contraste;
            localStorage.setItem('acc-contraste', configs.contraste);
            applyConfigurations();
        });
    }

    if (btnSemAnimacao) {
        btnSemAnimacao.addEventListener('click', () => {
            configs.semAnimacao = !configs.semAnimacao;
            localStorage.setItem('acc-sem-animacao', configs.semAnimacao);
            applyConfigurations();
        });
    }

    if (btnLeitorTela) {
        btnLeitorTela.addEventListener('click', () => {
            configs.leitorTela = !configs.leitorTela;
            localStorage.setItem('acc-leitor-tela', configs.leitorTela);
            applyConfigurations();
        });
    }

    // Lógica do Leitor de Tela (Text-to-Speech)
    let speechTimer;
    document.addEventListener('mouseover', function(e) {
        if (!configs.leitorTela) return;
        
        const target = e.target;
        // Ignorar o painel de acessibilidade para não ler os próprios botões
        if (target.closest('.accessibility-panel') || target.closest('.accessibility-btn')) return;

        // Limpar o conteúdo textual para leitura
        let textToRead = target.innerText || target.alt || target.title;
        
        // Evitar ler elementos muito grandes se houver filhos sendo lidos
        if (target.children.length > 2) return;

        if (textToRead && textToRead.trim() !== '') {
            clearTimeout(speechTimer);
            speechTimer = setTimeout(() => {
                if ('speechSynthesis' in window && window.speechSynthesis) {
                    window.speechSynthesis.cancel();
                    const utterance = new SpeechSynthesisUtterance(textToRead);
                    utterance.lang = 'pt-BR';
                    utterance.rate = 1.0;
                    window.speechSynthesis.speak(utterance);
                }
            }, 400); // Aguarda 400ms com o mouse em cima para iniciar a leitura
        }
    });

    document.addEventListener('mouseout', function() {
        if (configs.leitorTela) {
            clearTimeout(speechTimer);
        }
    });
});
