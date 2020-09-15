from invoke import task


@task
def build_frontend_debug(c):
    print('Building frontend (in debug mode)...')
    static_dir = 'mind_palace/mind_palace_main/static'
    c.run(f'mkdir -p {static_dir}')
    with c.cd('frontend'):
        c.run('npm run build')
        c.run(f'cp -v dist/site.js ../{static_dir}')
        c.run(f'cp -v dist/site.js.map ../{static_dir}')
        c.run(f'cp -v dist/site.css ../{static_dir}')


@task
def build_frontend_release(c):
    print('Building frontend (in release mode)...')
    static_dir = 'mind_palace/mind_palace_main/static'
    c.run(f'mkdir -p {static_dir}')
    with c.cd('frontend'):
        c.run('npm run buildprod')
        c.run(f'cp -v dist/site.js ../{static_dir}')
        c.run(f'cp -v dist/site.css ../{static_dir}')


@task(pre=[build_frontend_debug])
def collectstatic(c):
    c.run('python manage.py collectstatic --noinput')


@task(pre=[build_frontend_release])
def build(c):
    c.run('python setup.py sdist bdist_wheel')


def clean(c):
    c.run('rm -rf dist/ mind_palace.egg-info/ build/')
    c.run('rm mind_palace/mind_palace_main/static/site*')
