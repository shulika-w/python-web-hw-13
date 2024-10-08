from pydantic import UUID4
from typing import List

from fastapi import APIRouter, HTTPException, Depends, Query, Path, status

from src.database.connect_db import AsyncDBSession, get_session
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.schemas.contacts import ContactModel, ContactResponse
from src.services.auth import auth_service


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=1000),
    first_name: str = Query(default=None),
    last_name: str = Query(default=None),
    email: str = Query(default=None),
    user: User = Depends(auth_service.get_current_user),
    session: AsyncDBSession = Depends(get_session),
):
    return await repository_contacts.read_contacts(
        offset, limit, first_name, last_name, email, user, session
    )


@router.get("/birthdays_in_{n}_days", response_model=List[ContactResponse])
async def read_contacts_with_birthdays_in_n_days(
    n: int = Path(ge=1, le=31),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=1000),
    user: User = Depends(auth_service.get_current_user),
    session: AsyncDBSession = Depends(get_session),
):
    return await repository_contacts.read_contacts_with_birthdays_in_n_days(
        n, offset, limit, user, session
    )


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(
    contact_id: UUID4,
    user: User = Depends(auth_service.get_current_user),
    session: AsyncDBSession = Depends(get_session),
):
    contact = await repository_contacts.read_contact(contact_id, user, session)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    body: ContactModel,
    user: User = Depends(auth_service.get_current_user),
    session: AsyncDBSession = Depends(get_session),
):
    contact = await repository_contacts.create_contact(body, user, session)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The contact's email and/or phone already exist",
        )
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: UUID4,
    body: ContactModel,
    user: User = Depends(auth_service.get_current_user),
    session: AsyncDBSession = Depends(get_session),
):
    contact = await repository_contacts.update_contact(contact_id, body, user, session)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: UUID4,
    user: User = Depends(auth_service.get_current_user),
    session: AsyncDBSession = Depends(get_session),
):
    contact = await repository_contacts.delete_contact(contact_id, user, session)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return None