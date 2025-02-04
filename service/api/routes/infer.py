from fastapi import APIRouter, HTTPException, File, UploadFile, Depends, Request
import torch
import io
from PIL import Image


infer_router = APIRouter()

# Labels do modelo
labels = ["Cilindro", "Cone", "Esfera", "Nao definido", "Paralelepipedo", "Superficie"]
id2label = {i: label for i, label in enumerate(labels)}


@infer_router.post(
    "/resnet3d",
    summary="Classificação de Formas Geométricas 3D",
    description=(
        "Este endpoint recebe uma **imagem de um objeto tridimensional** e retorna "
        "a **classe predita** pelo modelo de **reconhecimento de formas 3D**. "
        "O modelo utilizado é baseado na arquitetura **ResNet-50**.\n\n"
        "🔹 **Classes possíveis:**\n"
        "- Cilindro\n"
        "- Cone\n"
        "- Esfera\n"
        "- Não definido\n"
        "- Paralelepípedo\n"
        "- Superfície\n\n"
        "📤 **Formato de Entrada:**\n"
        "- A requisição deve conter um arquivo de **imagem (JPEG/PNG)**.\n\n"
        "📥 **Formato de Saída:**\n"
        "```json\n"
        "{\n"
        '    "prediction": "Esfera"\n'
        "}\n"
        "```"
    ),
    response_description="A classe predita para a imagem enviada.",
)
async def resnet3d(
    request: Request,
    file: UploadFile = File(...),
):
    """
    Executa inferência em uma imagem enviada e retorna a classe predita.

    ### **Parâmetros**
    - `file` (UploadFile): Arquivo de imagem enviado para inferência (JPEG ou PNG).

    ### **Retorno**
    - JSON com a classe predita do objeto tridimensional.

    ### **Exemplo de Resposta**
    ```json
    {
        "prediction": "Cilindro"
    }
    ```
    """
    try:
        # Verifica se o arquivo é uma imagem válida
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="O arquivo enviado não é uma imagem válida.")

        # Lê a imagem do arquivo recebido
        image = Image.open(io.BytesIO(await file.read()))

        # **Aplica resize para 224x224, tamanho padrão da ResNet**
        image = image.resize((224, 224), Image.BICUBIC)

        # Processa a imagem
        encoded_image = request.app.state.feature_extractor(
            image.convert("RGB"), return_tensors="pt"
        )["pixel_values"]

        # Executa a inferência
        with torch.no_grad():
            logits = request.app.state.model(encoded_image).logits

        # Retorna a classe predita
        predicted_label = id2label[logits.argmax(-1).item()]
        return {"prediction": predicted_label}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
