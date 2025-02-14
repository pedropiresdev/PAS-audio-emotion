# Detecção e Classificação de Emoções em Falas de Vídeo

## Modelagem Arquitetural
A abordagem utilizada na documentação será o Modelo C4, criado por Simon Brown. O nome C4 vem das 4 
camadas de diagrama que ele propõe.

Esta abordagem possui alguns benefícios como a **simplicidade**, evitando diagramas excessivamente complexos, 
**hierarquia clara**, propiciando à diversos atores envolvidos a visão adequada do sistema, **padronização** que 
auxilia a comunicação entre equipes e a **independência de ferramentas**, podendo utilizar UMLs, diagramas 
desenhados a mão, Structurizr, etc.

### Diagrama de Contexto
Mostra uma visão de alto nível do sistema, incluindo usuários e sistemas externos com os quais interage.

### Diagrama de Contêiner
Divide o sistemas em contêineres e demonstra suas interações

### Diagrama de Componente
Detalha os componentes dentro de um contêiner e suas interações

### Diagrama de Código
_opcional_ 

Mostra detalhes da implementação no nível de código. Classes, métodos, etc. 

## Problema Proposto
- Criar uma aplicação web capaz de receber arquivos de mídia (áudio e vídeo) de usuários;
- Analisar o conteúdo;
- Retornar uma análise das emoções identificadas no arquivo baseadas no tom de voz do interlocutor. 

A análise será possível utilizando ferramentas de Inteligência Artificial.

## Solução Proposta
O software será desenvolvido em FastAPI, utilizando a linguagem de programação **Python**.

**Esse software poderá receber 3 tipos de entradas**:
* Áudio gravado pelo usuário diretamente no site
* Arquivo em áudio upado pelo usuário
* Arquivo em vídeo upado pelo usuário

Será utilizada a biblioteca **_Librosa_**, especialmente útil para extrair características 
de som como mel-frequency cepstral coefficients (**MFCCs**), comumente usados na análise de emoções. 
Dependendo do desempenho, podemos utilizar também a biblioteca **_OpenSMILE_** para a mesma finalidade.

Para **aprendizado de máquina**, há expectativa de utilizar as bibliotecas **_TensorFlow_** ou **_Keras_**. 
Contudo, dependendo do nível de complexidade da implementação, talvez utilizemos bibliotecas como 
**_pyAudioAnalysis_** ou **_Vokaturi_**, que oferecem implementações de modelos de detecção de emoções já treinados.

Após análise do material disponibilizado pelo usuário, aparecerá um prompt na tela 
descrevendo as emoções identificadas no arquivo.

## Diagrama de Contexto
**Descrição**: O sistema recebe um áudio ou vídeo de um usuário, processa o som para extrair características 
relevantes usando **librosa** e realiza a análise emocional.

### Principais atores envolvidos
**Usuário**: Envia arquivos de áudio ou vídeo;

**Sistema de Análise de Emoções (FastAPI)**: Processa o arquivo e extrai emoções;

**Serviço de Armazenamento**: Para salvar os arquivos temporariamente. Obs.: Esta implementação é opcional pois os 
arquivos podem ser escritos em tempo de execução na memória da aplicação e descartado após retorno da análise;

**Modelo de IA**: Analisa o tom de voz e retorna emoções detectadas.

![diagrama_contexto_b6](https://github.com/user-attachments/assets/f73925c4-78ce-4726-9556-af478760ff10)


