FROM kartoza/qgis-server:LTR

RUN rm /etc/apache2/conf-enabled/qgis.conf
ADD conf-available/qgis.conf /etc/apache2/conf-available/qgis.conf
RUN a2enconf qgis
CMD ["apache2", "-DFOREGROUND"]
