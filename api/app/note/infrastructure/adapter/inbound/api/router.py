from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from ulid import ULID  # type: ignore

from app.di.application.usecase import (
    get_create_note_draft_usecase,
    get_create_note_usecase,
    get_create_tag_usecase,
    get_delete_note_usecase,
    get_get_note_usecase,
    get_get_notes_usecase,
    get_list_tags_usecase,
    get_update_note_usecase,
    get_update_tag_usecase,
)
from app.note.application.command import UpdateNoteCommand, UpdateTagCommand
from app.note.application.usecase import (
    CreateNoteDraftUseCase,
    CreateNoteUseCase,
    CreateTagUseCase,
    DeleteNoteUseCase,
    GetNotesUseCase,
    GetNoteUseCase,
    ListTagsUseCase,
    UpdateNoteUseCase,
    UpdateTagUseCase,
)
from app.note.domain.entity import Note, Tag
from app.note.infrastructure.adapter.inbound.api.message import (
    CreateNoteDraftRequest,
    CreateNoteRequest,
    CreateNoteResponse,
    CreateTagRequest,
    CreateTagResponse,
    GetNoteResponse,
    GetNotesResponse,
    GetTagsResponse,
    PatchNoteRequest,
    PatchNoteResponse,
    PatchTagRequest,
    PatchTagResponse,
)

router: APIRouter = APIRouter(tags=["Note"])


@router.post("/draft", status_code=status.HTTP_201_CREATED)
def create_note_draft(
    request_model: CreateNoteDraftRequest,
    usecase: Annotated[CreateNoteDraftUseCase, Depends(get_create_note_draft_usecase)],
):
    note_draft: Note = usecase(user_id=request_model.created_by)

    return note_draft


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CreateNoteResponse)
def create_note(
    request_model: CreateNoteRequest, usecase: Annotated[CreateNoteUseCase, Depends(get_create_note_usecase)]
):
    note: Note = usecase(note_draft_id=request_model.note_draft_id, title=request_model.title)

    return CreateNoteResponse.from_model(note)


@router.post("/tag", status_code=status.HTTP_201_CREATED, response_model=CreateTagResponse)
def create_tag(request_model: CreateTagRequest, usecase: Annotated[CreateTagUseCase, Depends(get_create_tag_usecase)]):
    tag: Tag = usecase(name=request_model.name)

    return tag


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: ULID, usecase: Annotated[DeleteNoteUseCase, Depends(get_delete_note_usecase)]):
    try:
        usecase(note_id=note_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("", status_code=status.HTTP_200_OK, response_model=GetNotesResponse)
def get_notes(
    usecase: Annotated[GetNotesUseCase, Depends(get_get_notes_usecase)], page: int = 1, items_per_page: int = 10
):
    total_cnt, notes = usecase(page=page, items_per_page=items_per_page)
    return GetNotesResponse(total_cnt=total_cnt, page=page, notes=[GetNoteResponse.from_model(note) for note in notes])


@router.get("/detail/{note_id}", status_code=status.HTTP_200_OK, response_model=GetNoteResponse)
def get_note(note_id: ULID, usecase: Annotated[GetNoteUseCase, Depends(get_get_note_usecase)]):
    try:
        note: Note = usecase(note_id=note_id)
        return GetNoteResponse.from_model(note)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/tag", status_code=status.HTTP_200_OK, response_model=GetTagsResponse)
def get_tags(usecase: Annotated[ListTagsUseCase, Depends(get_list_tags_usecase)]):
    tags: list[Tag] = usecase()
    return GetTagsResponse(tags=tags)


@router.patch("/{note_id}", status_code=status.HTTP_200_OK, response_model=PatchNoteResponse)
def patch_note(
    note_id: ULID,
    request_model: PatchNoteRequest,
    usecase: Annotated[UpdateNoteUseCase, Depends(get_update_note_usecase)],
):
    cmd: UpdateNoteCommand = UpdateNoteCommand(
        id=note_id,
        user_id=request_model.user_id,
        title=request_model.title,
        content=request_model.content,
        tag_ids=request_model.tag_ids,
        status=request_model.status,
    )

    try:
        updated: Note = usecase(cmd=cmd)
        return PatchNoteResponse(
            title=updated.title,
            content=updated.content,
            updated_at=updated.updated_at,
            updated_by=updated.updated_by,
            tags=updated.tags,
            status=updated.status,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/tag/{tag_id}", status_code=status.HTTP_200_OK, response_model=PatchTagResponse)
def patch_tag(
    tag_id: ULID, request_model: PatchTagRequest, usecase: Annotated[UpdateTagUseCase, Depends(get_update_tag_usecase)]
):
    cmd: UpdateTagCommand = UpdateTagCommand(id=tag_id, name=request_model.name)

    try:
        updated: Tag = usecase(cmd=cmd)
        return PatchTagResponse(name=updated.name, updated_at=updated.updated_at)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
