### Asignación de permisos de ejecución

#Actualización de git
chmod +X ktbo-bi/Middleware/Mediaplan/git_update.sh

#actualización de planes de medios
chmod +X ktbo-bi/Middleware/Mediaplan/mp_dailychecker.sh

#actualización de matchrate a integrar con el mp_dailychecker
chmod +X ktbo-bi/Middleware/Mediaplan/matchrate_upd.sh

#validación diaria de todos los scripts menores
chmod +X ktbo-bi/Scripting/daily_val.sh

#descarga de las carpetas de sftp uploads/test para validación de matchrate
chmod +X ktbo-bi/Middleware/Campaigns/sftp_downloads.sh
