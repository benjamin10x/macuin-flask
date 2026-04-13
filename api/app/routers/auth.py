from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app import auth, models, schemas

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post("/login", response_model=schemas.TokenResponse)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(models.Usuario).filter(models.Usuario.email == form.username).first()
    if not user or not auth.verify_password(form.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos.",
        )
    token = auth.create_access_token({"sub": str(user.id)})
    return schemas.TokenResponse(
        access_token=token,
        user=schemas.UsuarioOut.model_validate(user),
    )


@router.post("/register", response_model=schemas.UsuarioOut, status_code=201)
def register(payload: schemas.RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(models.Usuario).filter(models.Usuario.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")
    user = models.Usuario(
        nombre=payload.nombre,
        email=payload.email,
        telefono=payload.telefono,
        password_hash=auth.hash_password(payload.password),
        rol="cliente",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/me", response_model=schemas.UsuarioOut)
def me(current_user: models.Usuario = Depends(auth.get_current_user)):
    return current_user
