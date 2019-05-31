from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import os


class DnDBeyond:
    driver_path = '{}/drivers/chromedriver'.format

    def scrape(self, url):
        output = {}
        cwd = os.getcwd()
        try:
            driver = webdriver.Chrome(self.driver_path(cwd))
        except WebDriverException:
            driver = webdriver.Chrome(self.driver_path(cwd + '/code'))
        # make window long to avoid mobile view
        driver.set_window_size(width=2000, height=1000)
        driver.get(url)

        # wait for content to load
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.ct-character-tidbits__name'))
            )

        name = driver.find_element_by_css_selector('.ct-character-tidbits__name')
        output['name'] = name.text

        stats = driver.find_elements_by_css_selector('.ct-ability-summary')
        output['stats'] = self.get_stats(stats)

        attacks = driver.find_elements_by_css_selector('.ct-combat-attack')
        output['attacks'] = self.get_attacks(attacks)

        skills = driver.find_elements_by_css_selector('.ct-skills__item')
        output['skills'] = self.get_skills(skills)
        driver.close()
        return output


    def get_skills(self, skills):
        output = {}
        for skill in skills:
            skillName = skill.find_element_by_css_selector(".ct-skills__col--skill").text
            modValue = self.get_modifier(skill)
            output[skillName] = modValue

        return output

    def get_attacks(self, attacks):
        output = {}
        for attack in attacks:
            name = attack.find_element_by_css_selector(".ct-combat-attack__label").text
            hit_mod_element = attack.find_element_by_css_selector(".ct-combat-attack__action")
            damage = attack.find_element_by_css_selector(".class='ct-combat-attack__damage").text
            try:
                hit_mod = self.get_modifier(hit_mod_element)
                output[name] = {
                    'hit': hit_mod,
                    'damage': damage,
                }
            except TypeError:
                # has a difficulty save
                save_details = attack.find_element_by_css_selector(".ct-combat-attack__action").text
                attacks[name] = {'save': save_details,
                                 'damage': damage}

        return output

    def get_modifier(self, element):
        symbol = element.find_element_by_css_selector('.ct-signed-number__sign').text
        value = element.find_element_by_css_selector('.ct-signed-number__number').text
        return int(symbol + value)

    def get_stats(self, stats):
        stat_mods = {}
        for stat in stats:
            title = stat.find_element_by_css_selector('.ct-ability-summary__label').text
            mod_value = self.get_modifier(stats)
            stat_mods[title] = mod_value

        return stat_mods