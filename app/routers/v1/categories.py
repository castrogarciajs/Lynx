from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.schemas import models, types
from app.deps import get_db, get_current_user
import cloudinary
import cloudinary.uploader

router = APIRouter()


@router.post("/create")
async def create_category(
    category: types.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_category = category.model_dump()

    user = (
        db.query(models.User).filter(models.User.email == current_user["sub"]).first()
    )

    if not user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "You do not have permission to create category",
                "db": [],
                "status": status.HTTP_400_BAD_REQUEST,
            },
        )
    cloudinary.uploader.upload(
        "https://cloudinary-devs.github.io/cld-docs-assets/assets/images/butterfly.jpeg",
        public_id="quickstart_butterfly",
        unique_filename=False,
        overwrite=True,
    )

    srcURL = cloudinary.CloudinaryImage("quickstart_butterfly").build_url()

    print("Url image", srcURL, "\n")

    db_user = models.Category(
        name=user_category["name"],
        image=srcURL,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "message": "new category was created",
        "status": status.HTTP_200_OK,
    }
