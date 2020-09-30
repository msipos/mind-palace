from invoke import task

STATIC_DIR = 'mind_palace/mind_palace_main/static'


@task
def build_frontend_debug(c):
    print('Building frontend (in debug mode)...')
    c.run(f'mkdir -p {STATIC_DIR}')
    with c.cd('frontend'):
        c.run('npm run build')
        c.run(f'cp -v dist/site.js ../{STATIC_DIR}')
        c.run(f'cp -v dist/site.js.map ../{STATIC_DIR}')
        c.run(f'cp -v dist/site.css ../{STATIC_DIR}')
        c.run(f'cp -vR static_assets/* ../{STATIC_DIR}')


@task
def build_frontend_release(c):
    print('Building frontend (in release mode)...')
    c.run(f'mkdir -p {STATIC_DIR}')
    with c.cd('frontend'):
        c.run('npm run buildprod')
        c.run(f'cp -v dist/site.js ../{STATIC_DIR}')
        c.run(f'cp -v dist/site.css ../{STATIC_DIR}')
        c.run(f'cp -vR static_assets/* ../{STATIC_DIR}')


@task(pre=[build_frontend_debug])
def collectstatic(c):
    c.run('python manage.py collectstatic --noinput')


@task(pre=[build_frontend_release])
def build(c):
    c.run('python setup.py sdist bdist_wheel')


@task
def clean(c):
    c.run('rm -rfv dist/ mind_palace.egg-info/ build/')
    c.run('rm -rfv mind_palace/mind_palace_main/static/*')
