# syntax=docker/dockerfile:1
# Custom Odoo 17 image with our Arabic eLearning course modules baked in.
# Build:  docker build -t odoo-elearning-lab:latest .
FROM odoo:17.0

LABEL org.opencontainers.image.title="odoo-elearning-lab" \
      org.opencontainers.image.description="Odoo 17 eLearning with Arabic sample courses (learning project)" \
      org.opencontainers.image.licenses="MIT"

USER root

# Extra Python packages for our addons go here (none needed today).
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt || \
    pip3 install --no-cache-dir --break-system-packages -r /tmp/requirements.txt

# Our custom addons live in their own folder, separate from Odoo's core addons.
COPY --chown=odoo:odoo ./addons /mnt/extra-addons
COPY --chown=odoo:odoo ./config/odoo.conf /etc/odoo/odoo.conf

USER odoo

# Odoo answers on 8069 (HTTP) and 8072 (long-polling / websockets).
EXPOSE 8069 8072

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=5 \
  CMD python3 -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8069/web/health', timeout=4).status==200 else 1)"
