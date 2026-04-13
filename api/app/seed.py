from __future__ import annotations

from app.database import SessionLocal
from app import models
from app.auth import hash_password

AUTOPARTES = [
    {"nombre": "Filtro de aceite Premium", "categoria": "Filtros", "precio": 125.00, "stock": 50, "stock_minimo": 5, "descripcion": "Filtro de aceite de alta calidad para motores modernos", "marca": "Bosch"},
    {"nombre": "Filtro de aire deportivo", "categoria": "Filtros", "precio": 280.00, "stock": 35, "stock_minimo": 5, "descripcion": "Mayor flujo de aire para mejor rendimiento", "marca": "K&N"},
    {"nombre": "Filtro de combustible", "categoria": "Filtros", "precio": 95.00, "stock": 60, "stock_minimo": 8, "descripcion": "Filtro de combustible universal", "marca": "Purolator"},
    {"nombre": "Pastillas de freno delanteras", "categoria": "Frenos", "precio": 450.00, "stock": 30, "stock_minimo": 5, "descripcion": "Pastillas de freno cerámicas de alto rendimiento", "marca": "Brembo"},
    {"nombre": "Disco de freno ventilado", "categoria": "Frenos", "precio": 890.00, "stock": 20, "stock_minimo": 3, "descripcion": "Disco ventilado para mejor disipación de calor", "marca": "Brembo"},
    {"nombre": "Pastillas de freno traseras", "categoria": "Frenos", "precio": 380.00, "stock": 25, "stock_minimo": 4, "descripcion": "Pastillas semimetálicas para frenos traseros", "marca": "Akebono"},
    {"nombre": "Bujías de iridio", "categoria": "Encendido", "precio": 180.00, "stock": 60, "stock_minimo": 10, "descripcion": "Bujías de iridio de larga duración", "marca": "NGK"},
    {"nombre": "Bobina de encendido", "categoria": "Encendido", "precio": 380.00, "stock": 12, "stock_minimo": 3, "descripcion": "Bobina de encendido de alto rendimiento", "marca": "Delphi"},
    {"nombre": "Alternador reconstruido", "categoria": "Electrico", "precio": 1200.00, "stock": 8, "stock_minimo": 2, "descripcion": "Alternador reconstruido con garantía de 1 año", "marca": "Remy"},
    {"nombre": "Motor de arranque", "categoria": "Electrico", "precio": 950.00, "stock": 6, "stock_minimo": 2, "descripcion": "Motor de arranque remanufacturado", "marca": "Bosch"},
    {"nombre": "Amortiguador delantero", "categoria": "Suspension", "precio": 750.00, "stock": 15, "stock_minimo": 3, "descripcion": "Amortiguador de gas de alto rendimiento", "marca": "KYB"},
    {"nombre": "Resorte de suspensión", "categoria": "Suspension", "precio": 320.00, "stock": 25, "stock_minimo": 4, "descripcion": "Resorte progresivo para mejor manejo", "marca": "Moog"},
    {"nombre": "Aceite de motor 5W-30", "categoria": "Lubricantes", "precio": 95.00, "stock": 100, "stock_minimo": 20, "descripcion": "Aceite sintético 5W-30 para motores modernos", "marca": "Castrol"},
    {"nombre": "Aceite de transmisión ATF", "categoria": "Lubricantes", "precio": 85.00, "stock": 45, "stock_minimo": 10, "descripcion": "Aceite para transmisión automática Dexron III", "marca": "Valvoline"},
    {"nombre": "Radiador de aluminio", "categoria": "Refrigeracion", "precio": 1800.00, "stock": 6, "stock_minimo": 2, "descripcion": "Radiador de aluminio de alta eficiencia", "marca": "Mishimoto"},
    {"nombre": "Termostato 88°C", "categoria": "Refrigeracion", "precio": 120.00, "stock": 40, "stock_minimo": 8, "descripcion": "Termostato estándar de 88 grados Celsius"},
    {"nombre": "Bomba de agua", "categoria": "Refrigeracion", "precio": 450.00, "stock": 18, "stock_minimo": 3, "descripcion": "Bomba de agua de repuesto directo", "marca": "Gates"},
]


def run_seed() -> None:
    db = SessionLocal()
    try:
        if db.query(models.Usuario).count() > 0:
            return

        admin = models.Usuario(
            nombre="Administrador MACUIN",
            email="admin@macuin.com",
            password_hash=hash_password("admin123"),
            rol="admin",
        )
        db.add(admin)

        for data in AUTOPARTES:
            db.add(models.Autoparte(
                nombre=data["nombre"],
                categoria=data["categoria"],
                precio=data["precio"],
                stock=data["stock"],
                stock_minimo=data.get("stock_minimo", 10),
                descripcion=data.get("descripcion"),
                marca=data.get("marca"),
                activo=True,
            ))

        db.commit()
        print("Seed completado: admin@macuin.com / admin123")
    except Exception as exc:
        print(f"Error en seed: {exc}")
        db.rollback()
    finally:
        db.close()
