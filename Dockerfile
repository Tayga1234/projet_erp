FROM odoo:16

# Set environment variables
ENV HOST=medical-db
ENV PORT=8069
ENV USER=odoo
ENV PASSWORD=odoo123
ENV DB_NAME=medical_db

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy custom addons
COPY ./addons /mnt/extra-addons
COPY ./requirements.txt /tmp/

# Install Python dependencies if any
RUN pip3 install -r /tmp/requirements.txt || true

# Set permissions
RUN chown -R odoo:odoo /mnt/extra-addons

# Expose port
EXPOSE 8069

# Default command
CMD ["odoo", "--db_host=$HOST", "--db_port=5432", "--db_user=$USER", "--db_password=$PASSWORD", "--database=$DB_NAME", "--dev=all"]
