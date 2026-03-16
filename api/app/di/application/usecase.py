from fastapi import Depends  # type: ignore

from app.auth.application.usecase import (
    ChangeRoleUseCase,
    RefreshCredentialsUseCase,
    SignInUseCase,
    SignOutUseCase,
    SignUpUseCase,
    VerifyCredentialsUseCase,
    VerifyPasswordUseCase,
)
from app.di.domain.repository import (
    get_credentials_repository,
    get_note_repository,
    get_principal_repository,
    get_tag_repository,
    get_user_repository,
)
from app.di.domain.service import get_authentication_service, get_password_hasher
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
from app.note.domain.repository import NoteRepository, TagRepository
from app.user.application.usecase import CreateUserUseCase, DeleteUserUseCase, GetUsersUseCase, UpdateUserUseCase
from app.user.domain.repository import UserRepository
from core.auth.domain.repository import CredentialsRepository, PrincipalRepository
from core.auth.domain.service import AuthenticationService
from core.auth.infrastructure.service import BcryptPasswordHasher


def get_create_user_usecase(user_repo: UserRepository = Depends(get_user_repository)) -> CreateUserUseCase:
    return CreateUserUseCase(user_repo=user_repo)


def get_update_user_usecase(user_repo: UserRepository = Depends(get_user_repository)) -> UpdateUserUseCase:
    return UpdateUserUseCase(user_repo=user_repo)


def get_get_users_usecase(user_repo: UserRepository = Depends(get_user_repository)) -> GetUsersUseCase:
    return GetUsersUseCase(user_repo=user_repo)


def get_delete_user_usecase(
    user_repo: UserRepository = Depends(get_user_repository),
    credentials_repo: CredentialsRepository = Depends(get_credentials_repository),
    principal_repo: PrincipalRepository = Depends(get_principal_repository),
) -> DeleteUserUseCase:
    return DeleteUserUseCase(user_repo=user_repo, credentials_repo=credentials_repo, principal_repo=principal_repo)


def get_sign_in_usecase(
    auth_service: AuthenticationService = Depends(get_authentication_service),
    user_repo: UserRepository = Depends(get_user_repository),
) -> SignInUseCase:
    return SignInUseCase(auth_service=auth_service, user_repo=user_repo)


def get_sign_out_usecase(
    auth_service: AuthenticationService = Depends(get_authentication_service),
    user_repo: UserRepository = Depends(get_user_repository),
) -> SignOutUseCase:
    return SignOutUseCase(auth_service=auth_service, user_repo=user_repo)


def get_verify_credentials_usecase(
    auth_service: AuthenticationService = Depends(get_authentication_service),
    user_repo: UserRepository = Depends(get_user_repository),
) -> VerifyCredentialsUseCase:
    return VerifyCredentialsUseCase(auth_service=auth_service, user_repo=user_repo)


def get_refresh_credentials_usecase(
    auth_service: AuthenticationService = Depends(get_authentication_service),
) -> RefreshCredentialsUseCase:
    return RefreshCredentialsUseCase(auth_service=auth_service)


def get_verify_password_usecase(
    principal_repo: PrincipalRepository = Depends(get_principal_repository),
    password_hasher: BcryptPasswordHasher = Depends(get_password_hasher),
) -> VerifyPasswordUseCase:
    return VerifyPasswordUseCase(principal_repo=principal_repo, password_hasher=password_hasher)


def get_sign_up_usecase(
    auth_service: AuthenticationService = Depends(get_authentication_service),
    password_hasher: BcryptPasswordHasher = Depends(get_password_hasher),
    principal_repo: PrincipalRepository = Depends(get_principal_repository),
    user_repo: UserRepository = Depends(get_user_repository),
) -> SignUpUseCase:
    return SignUpUseCase(
        auth_service=auth_service, password_hasher=password_hasher, principal_repo=principal_repo, user_repo=user_repo
    )


def get_change_role_usecase(
    principal_repo: PrincipalRepository = Depends(get_principal_repository),
    user_repo: UserRepository = Depends(get_user_repository),
) -> ChangeRoleUseCase:
    return ChangeRoleUseCase(principal_repo=principal_repo, user_repo=user_repo)


def get_create_note_draft_usecase(
    note_repo: NoteRepository = Depends(get_note_repository), tag_repo: TagRepository = Depends(get_tag_repository)
) -> CreateNoteDraftUseCase:
    return CreateNoteDraftUseCase(note_repo=note_repo, tag_repo=tag_repo)


def get_create_note_usecase(note_repo: NoteRepository = Depends(get_note_repository)) -> CreateNoteUseCase:
    return CreateNoteUseCase(note_repo=note_repo)


def get_create_tag_usecase(tag_repo: TagRepository = Depends(get_tag_repository)) -> CreateTagUseCase:
    return CreateTagUseCase(tag_repo=tag_repo)


def get_delete_note_usecase(
    note_repo: NoteRepository = Depends(get_note_repository),
    credentials_repo: CredentialsRepository = Depends(get_credentials_repository),
    principal_repo: PrincipalRepository = Depends(get_principal_repository),
) -> DeleteNoteUseCase:
    return DeleteNoteUseCase(note_repo=note_repo)


def get_get_notes_usecase(note_repo: NoteRepository = Depends(get_note_repository)) -> GetNotesUseCase:
    return GetNotesUseCase(note_repo=note_repo)


def get_get_note_usecase(note_repo: NoteRepository = Depends(get_note_repository)) -> GetNoteUseCase:
    return GetNoteUseCase(note_repo=note_repo)


def get_list_tags_usecase(tag_repo: TagRepository = Depends(get_tag_repository)) -> ListTagsUseCase:
    return ListTagsUseCase(tag_repo=tag_repo)


def get_update_note_usecase(
    note_repo: NoteRepository = Depends(get_note_repository), tag_repo: TagRepository = Depends(get_tag_repository)
) -> UpdateNoteUseCase:
    return UpdateNoteUseCase(note_repo=note_repo, tag_repo=tag_repo)


def get_update_tag_usecase(tag_repo: TagRepository = Depends(get_tag_repository)) -> UpdateTagUseCase:
    return UpdateTagUseCase(tag_repo=tag_repo)
