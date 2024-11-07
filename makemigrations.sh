#!/bin/bash

# Function to log messages with timestamps and separators
log() {
  echo "----------------------------------------" | tee -a makemigrations.log
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a makemigrations.log
}
starting_log() {
  echo "########################################" | tee -a makemigrations.log
  echo "########################################" | tee -a makemigrations.log
  echo "########################################" | tee -a makemigrations.log
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a makemigrations.log
}

# Check if the virtual environment is active
starting_log "Starting makemigrations script..."
if [[ -z "$VIRTUAL_ENV" ]]; then
  log "Please activate the virtual environment before running this script."
  read -p "Press any key to close the window..."
  exit 1
fi

# Check if Django is available
if ! python -c "import django" &> /dev/null; then
  log "Django is not installed in the current environment."
  read -p "Press any key to close the window..."
  exit 1
fi

# Configure the Django environment
export DJANGO_SETTINGS_MODULE="edplatform.settings"

# Function to run makemigrations and migrate for a list of apps
run_migrations() {
  local apps=("$@")
  for app in "${apps[@]}"; do
    log "Running makemigrations for $app"
    python manage.py makemigrations "$app" | tee -a makemigrations.log
    if [[ $? -ne 0 ]]; then
      log "Error during makemigrations for app $app"
      read -p "Press any key to close the window..."
      exit 1
    fi
    log "Migrating app: $app"
    python manage.py migrate "$app" | tee -a makemigrations.log || {
      if [[ $? -eq 1 ]]; then
        log "App '$app' does not have migrations. Ignoring error and continuing..."
      else
        log "Error during migration for app $app"
        read -p "Press any key to close the window..."
        exit 1
      fi
    }
  done
}

# Extract the apps from settings.py and remove "django.contrib." prefix
DJANGO_MODULES=($(python -c "from edplatform.settings import DJANGO_MODULES; print(' '.join([app.replace('django.contrib.', '') for app in DJANGO_MODULES]))"))
CORE_MODULES=($(python -c "from edplatform.settings import CORE_MODULES; print(' '.join([app.replace('core_modules.', '') for app in CORE_MODULES]))"))
CUSTOM_MODULES=($(python -c "from edplatform.settings import CUSTOM_MODULES; print(' '.join(CUSTOM_MODULES))"))

# Run migrations for DJANGO_MODULES
log "Running migrations for DJANGO_MODULES..."
run_migrations "${DJANGO_MODULES[@]}"

# Run migrations for CORE_MODULES
log "Running migrations for CORE_MODULES..."
run_migrations "${CORE_MODULES[@]}"

# Run migrations for CUSTOM_MODULES
log "Running migrations for CUSTOM_MODULES..."
log "CUSTOM_MODULES: ${CUSTOM_MODULES[*]}"
run_migrations "${CUSTOM_MODULES[@]}"

log "Migrations completed for all apps."

# Keep the window open
read -p "Press any key to close the window..."