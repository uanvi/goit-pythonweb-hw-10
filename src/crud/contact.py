from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date, timedelta
from typing import List, Optional

from src.models.contact import Contact
from src.schemas.contact import ContactCreate, ContactUpdate

def create_contact(db: Session, contact: ContactCreate, user_id: int) -> Contact:
    """Створити новий контакт для користувача"""
    db_contact = Contact(**contact.dict(), user_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_user_contact(db: Session, contact_id: int, user_id: int) -> Optional[Contact]:
    """Отримати контакт користувача за ID"""
    return db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user_id)
    ).first()

def get_user_contacts(
    db: Session, 
    user_id: int,
    skip: int = 0, 
    limit: int = 100,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None
) -> List[Contact]:
    """Отримати список контактів користувача з фільтрацією"""
    query = db.query(Contact).filter(Contact.user_id == user_id)
    
    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    
    return query.offset(skip).limit(limit).all()

def update_contact(
    db: Session, 
    contact_id: int, 
    contact_update: ContactUpdate, 
    user_id: int
) -> Optional[Contact]:
    """Оновити контакт користувача"""
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user_id)
    ).first()
    
    if contact:
        for field, value in contact_update.dict().items():
            setattr(contact, field, value)
        db.commit()
        db.refresh(contact)
    return contact

def delete_contact(db: Session, contact_id: int, user_id: int) -> bool:
    """Видалити контакт користувача"""
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user_id)
    ).first()
    
    if contact:
        db.delete(contact)
        db.commit()
        return True
    return False

def get_user_upcoming_birthdays(db: Session, user_id: int) -> List[Contact]:
    """Отримати контакти користувача з днями народження на найближчі 7 днів"""
    today = date.today()
    next_week = today + timedelta(days=7)
    
    # Базовий запит для користувача
    base_query = db.query(Contact).filter(Contact.user_id == user_id)
    
    if today.year == next_week.year:
        # Якщо в межах одного року
        return base_query.filter(
            and_(Contact.birthday >= today, Contact.birthday <= next_week)
        ).all()
    else:
        # Обробка переходу між роками
        contacts_this_year = base_query.filter(
            and_(Contact.birthday >= today, Contact.birthday <= date(today.year, 12, 31))
        ).all()
        contacts_next_year = base_query.filter(
            and_(Contact.birthday >= date(next_week.year, 1, 1), Contact.birthday <= next_week)
        ).all()
        return contacts_this_year + contacts_next_year

def get_contact_by_email_and_user(db: Session, email: str, user_id: int) -> Optional[Contact]:
    """Отримати контакт користувача за email"""
    return db.query(Contact).filter(
        and_(Contact.email == email, Contact.user_id == user_id)
    ).first()