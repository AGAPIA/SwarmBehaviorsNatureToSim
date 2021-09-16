import carla

class WeatherBuilder():

    def get_weather_config(cloudiness= 3, precipitation = 0.0, precipitation_deposits = 0.0,
                sun_altitude_angle=45.0 ,sun_azimuth_angle= 30.0, wind_intensity  = 0.0,
                fog_density =0.5,
                fog_falloff=0.5,
                wetness=0
                ):


        return carla.WeatherParameters(cloudiness = cloudiness,
                precipitation_deposits=precipitation_deposits, precipitation= precipitation,
                sun_azimuth_angle= sun_azimuth_angle,sun_altitude_angle= sun_altitude_angle, 
                wind_intensity = wind_intensity, 
                fog_density = fog_density, fog_falloff = fog_falloff,
                wetness = wetness,
                )