from fastapi import APIRouter, Depends, UploadFile, File, Response

from uuid import UUID
import io
import zipfile

from services import PostcardService
from schemas.postcards import PostcardPreviewData

postcard_api_router = APIRouter()


@postcard_api_router.post("/preview")
async def preview(
        body: PostcardPreviewData = Depends(),
        file: UploadFile = File(...),
        postcard_service: PostcardService = Depends()
) -> Response:
    image_byte_array = await postcard_service.create_preview(file, body)
    return Response(
        content=image_byte_array,
        media_type="image/png"
    )


@postcard_api_router.post("/")
async def save_postcard(
        file: UploadFile = File(...),
        postcard_service: PostcardService = Depends()
) -> UUID:
    return await postcard_service.save(file)


@postcard_api_router.get("/")
async def get_postcards(
        postcard_service: PostcardService = Depends()
):
    arrays = await postcard_service.get_all()
    with io.BytesIO() as zip_buffer:
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for index, byte_data in enumerate(arrays):
                zipf.writestr(f'file_{index}.png', byte_data)

        zip_buffer.seek(0)

        response = Response(content=zip_buffer.read(), media_type="application/zip")
        response.headers["Content-Disposition"] = "attachment; filename=archive.zip"
        return response
