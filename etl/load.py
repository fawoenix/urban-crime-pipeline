import os, json
from sqlalchemy import create_engine, text

engine = create_engine(
f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

def load_data(df, bad):
    with engine.begin() as conn:
        for _, r in df.iterrows():
            conn.execute(text("""
                INSERT INTO crime_incidents (id, arrest, domestic, is_violent)
                VALUES (:id, :arrest, :domestic, :is_violent)
                ON CONFLICT (id) DO UPDATE SET arrest=EXCLUDED.arrest
            """), dict(id=int(r["id"]), arrest=r.get("arrest"), domestic=r.get("domestic"), is_violent=r.get("is_violent")))
        for b in bad:
            conn.execute(text("INSERT INTO bad_records (raw_data,error_reason) VALUES (:d,:r)"),
                         dict(d=json.dumps(b), r="validation_failed"))
