FROM odoo:16

# Copy custom addons
COPY ./addons /mnt/extra-addons

# Expose port
EXPOSE 8069

# Default command
CMD ["odoo", "--db_host=medical-db", "--db_port=5432", "--db_user=odoo", "--db_password=odoo123", "--database=medical_db", "--dev=all"]
