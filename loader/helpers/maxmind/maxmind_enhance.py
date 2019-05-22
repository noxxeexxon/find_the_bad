import geoip2.database

class Maxmind:
    def __init__(self):
        self.geo_db = geoip2.database.Reader('helpers/maxmind/databases/GeoLite2-City.mmdb')
        self.asn_db = geoip2.database.Reader('helpers/maxmind/databases/GeoLite2-ASN.mmdb')

    def get_geo(self, ip):
        '''
        returns the country and city for an IP
        '''
        geo_rec = {
            'country': 'Unknown',
            'city': 'Unknown',
            'location': '0, 0'
        }
        try:
            geo = self.geo_db.city(ip)
            if geo.country.name is not None:
                geo_rec['country'] = geo.country.name
            if geo.city.name is not None:
                geo_rec['city'] = geo.city.name
            if geo.location.latitude and geo.location.longitude:
                geo_rec['location'] =  "{0},{1}".format(format(geo.location.latitude, '.2f'), format(geo.location.longitude,'.2f'))
        except Exception as ex:
            # print(ex)
            pass
        return geo_rec

    def get_network(self, ip):
        network_rec = {
            'asn': -1,
            'org': 'Unknown'
        }
        try:
            network = self.asn_db.asn(ip)
            if network.autonomous_system_number is not None:
                network_rec['asn'] = network.autonomous_system_number
            if network.autonomous_system_organization is not None:
                network_rec['org'] = network.autonomous_system_organization
        except Exception as ex:
            # print(ex)
            pass

        return network_rec

    def get_maxmind_info(self, ip):
        geo_info = self.get_geo(ip)
        network_info = self.get_network(ip)
        maxmind_info = {
            'geo': geo_info,
            'network': network_info
        }
        return maxmind_info

    def close_geo_db(self):
        self.geo_db.close()

'''
if __name__ == "__main__":
    maxmind_lookup = Maxmind()
    lookup = maxmind_lookup.get_maxmind_info('128.101.101.101')
    print(lookup)
'''
