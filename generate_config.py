import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from jinja2 import Environment, FileSystemLoader

from app.models import sqlacodegen
from app.config import cfg


def get_session():
    engine = create_engine(cfg.SQLALCHEMY_DATABASE_URI,
                           pool_size=2,
                           pool_recycle=7200,
                           pool_pre_ping=True,
                           encoding='utf-8')

    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    return session


def main():
    session = get_session()
    results = session.query(sqlacodegen.Setting).filter_by(section="system").all()
    config = {key: getattr(cfg, key) for key in dir(cfg) if key.startswith("SUPERVISOR")}
    for result in results:
        config[result.key] = result.value

    tmpl_path = config["SUPERVISOR_TEMPLATE_PATH"]
    tmpl_folder = os.path.dirname(tmpl_path)
    tmpl_file = os.path.split(tmpl_path)[1]
    env = Environment(
        loader=FileSystemLoader(tmpl_folder),
        autoescape=False
    )
    template = env.get_template(tmpl_file)
    with open("supervisord.conf", "w") as f:
        f.write(template.render(**config))


if __name__ == "__main__":
    main()