from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .... import models


class DeviceCreate(BaseModel):
    name: str
    user_id: int


class DeviceResponse(BaseModel):
    id: int
    name: str
    user_id: int

    class ConfigDict:
        from_attributes = True


class Device:
    def create_device(device: DeviceCreate, db: Session):
        db_device = models.Device(name=device.name, user_id=device.user_id)
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        return db_device

    def get_device(user_id: int, db: Session):
        return db.query(models.Device).filter(models.Device.user_id == user_id).first()

    def delete_device(device_id: int, db: Session):
        db_device = (
            db.query(models.Device).filter(models.Device.id == device_id).first()
        )
        if db_device is None:
            raise HTTPException(status_code=404, detail="Device not found")
        db.delete(db_device)
        db.commit()
        return db_device
