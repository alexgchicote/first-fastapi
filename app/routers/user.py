from .. import models, schemas, utils
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    

    # raise exception if input_email is an existing email in the db
    input_email = db.query(models.User).filter(models.User.email == user.email).first()
    if input_email:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail=f'An account with this email has already been created')


    # has the password - can be retrieved from user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # add user to db using sqlalchemy
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} does not exist')

    return user