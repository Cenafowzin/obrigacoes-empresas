from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Empresa, ObrigacaoAcessoria
from schemas import EmpresaCreate, EmpresaResponse, ObrigacaoAcessoriaCreate, ObrigacaoAcessoriaResponse
from database import Base, engine, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/empresas/", response_model=EmpresaResponse)
def create_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.get("/empresas/", response_model=list[EmpresaResponse])
def get_empresas(db: Session = Depends(get_db)):
    return db.query(Empresa).all()

@app.get("/empresas/{empresa_id}", response_model=EmpresaResponse)
def get_empresa_by_id(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return db_empresa

@app.put("/empresas/{empresa_id}", response_model=EmpresaResponse)
def editar_empresa(empresa_id: int, empresa: EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    db_empresa.nome = empresa.nome
    db_empresa.cnpj = empresa.cnpj
    db_empresa.endereco = empresa.endereco
    db_empresa.email = empresa.email
    db_empresa.telefone = empresa.telefone
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.delete("/empresas/{empresa_id}", response_model=EmpresaResponse)
def excluir_empresa(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    db.delete(db_empresa)
    db.commit()
    return db_empresa

@app.post("/obrigacoes/", response_model=ObrigacaoAcessoriaResponse)
def create_obrigacao(obrigacao: ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).filter(Empresa.id == obrigacao.empresa_id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    db_obrigacao = ObrigacaoAcessoria(**obrigacao.dict())
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

@app.get("/obrigacoes/", response_model=list[ObrigacaoAcessoriaResponse])
def get_obrigacoes(db: Session = Depends(get_db)):
    return db.query(ObrigacaoAcessoria).all()

@app.get("/obrigacoes/{obrigacao_id}", response_model=ObrigacaoAcessoriaResponse)
def get_obrigacao_by_id(obrigacao_id: int, db: Session = Depends(get_db)):
    db_obrigacao = db.query(ObrigacaoAcessoria).filter(ObrigacaoAcessoria.id == obrigacao_id).first()
    if db_obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação Acessória não encontrada")
    return db_obrigacao

@app.put("/obrigacoes/{obrigacao_id}", response_model=ObrigacaoAcessoriaResponse)
def editar_obrigacao(obrigacao_id: int, obrigacao: ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    db_obrigacao = db.query(ObrigacaoAcessoria).filter(ObrigacaoAcessoria.id == obrigacao_id).first()
    if db_obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação Acessória não encontrada")

    db_obrigacao.nome = obrigacao.nome
    db_obrigacao.periodicidade = obrigacao.periodicidade
    db_obrigacao.empresa_id = obrigacao.empresa_id
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

@app.delete("/obrigacoes/{obrigacao_id}", response_model=ObrigacaoAcessoriaResponse)
def excluir_obrigacao(obrigacao_id: int, db: Session = Depends(get_db)):
    db_obrigacao = db.query(ObrigacaoAcessoria).filter(ObrigacaoAcessoria.id == obrigacao_id).first()
    if db_obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação Acessória não encontrada")

    db.delete(db_obrigacao)
    db.commit()
    return db_obrigacao
