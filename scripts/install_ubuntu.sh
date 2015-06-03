apt-get install                 \
    apache2                     \
    mysql-server                \
    libapache2-mod-wsgi         \
    libapache2-mod-jk           \
    python-cjson                \
    python-django               \
    python-django-piston        \
    python-mysqldb              \
    python-libxml2              \
    python-lxml                 \
    python-django-extensions    \
    python-django-extra-views   \
    python-imaging              \
    sqlite3                     \
    javascript-common           \
    libjs-jquery-ui             \
    libjs-jquery-timepicker
echo 'export MDS_DIR=/opt/sana/sana.mds' >> /etc/apache2/envvars