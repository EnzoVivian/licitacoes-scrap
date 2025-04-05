from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import csv
import json

def navigator_initializer():
    return webdriver.Firefox()

def cookies(browser):
    cookies = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "authorizeCookiesRememberLater")))
    cookies.click()

def fill_filters(browser):
    start_date = time.strftime("%d/%m/%Y", time.localtime(time.time() - 7276000))
    end_date = time.strftime("%d/%m/%Y", time.localtime(time.time() + 7276000))

    publicationStartDate = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "publicationStartDate")))
    publicationStartDate.send_keys("01/01/2024")

    publicationEndDate = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "publicationEndDate")))
    publicationEndDate.send_keys("01/01/2025")
    """
    status = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-id='status']")))
    status.click()

    dropdown_option = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Editais agendados']"))
    )
    dropdown_option.click()
    """
    family = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='s2id_autogen2']")))
    
    family.send_keys("0400")
    family.send_keys(Keys.ENTER)
    family.send_keys("0420")
    family.send_keys(Keys.ENTER)
    family.send_keys("0535")
    family.send_keys(Keys.ENTER)
    family.send_keys("0593")
    family.send_keys(Keys.ENTER)
    family.send_keys("0185")
    family.send_keys(Keys.ENTER)
    family.send_keys("0445")
    family.send_keys(Keys.ENTER)
    family.send_keys("0410")
    family.send_keys(Keys.ENTER)
    family.send_keys("0754")
    family.send_keys(Keys.ENTER)
    family.send_keys("0565")
    family.send_keys(Keys.ENTER)
    family.send_keys("0290")
    family.send_keys(Keys.ENTER)
    family.send_keys("0405")
    family.send_keys(Keys.ENTER)
    family.send_keys("0435")
    family.send_keys(Keys.ENTER)
    family.send_keys("0466")
    family.send_keys(Keys.ENTER)
    family.send_keys("0465")
    family.send_keys(Keys.ENTER)
    family.send_keys("0475")
    family.send_keys(Keys.ENTER)
    family.send_keys("0548")
    family.send_keys(Keys.ENTER)
    family.send_keys("0550")
    family.send_keys(Keys.ENTER)
    family.send_keys("0450")
    family.send_keys(Keys.ENTER)
    family.send_keys("0440")
    family.send_keys(Keys.ENTER)
    family.send_keys("460")
    family.send_keys(Keys.ENTER)
    family.send_keys("0034")
    family.send_keys(Keys.ENTER)
    family.send_keys(Keys.ENTER)
    family.send_keys("0750")
    family.send_keys(Keys.ENTER)
    family.send_keys("0463")
    family.send_keys(Keys.ENTER)
    family.send_keys("0990")
    family.send_keys(Keys.ENTER)
    family.send_keys("1002")
    family.send_keys(Keys.ENTER)
    family.send_keys("067")
    family.send_keys(Keys.ENTER)
    family.send_keys("0007")
    family.send_keys(Keys.ENTER)
    family.send_keys("0027")
    family.send_keys(Keys.ENTER)
    family.send_keys("0003")
    family.send_keys(Keys.ENTER)
    
    description = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='description']")))
    description.send_keys("")

    search = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='PsButton_pesquisar']")))
    search.click()

def collect_data(browser):
    browser.get("https://www.compras.rs.gov.br/editais/pesquisar")
    browser.maximize_window()
    cookies(browser)
    fill_filters(browser)
    licitations = []
    while True:
        time.sleep(10)
        licitations_table = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//table[@id='procurementsDatatable']/tbody/tr/td"))
        )
        for i in range(0, len(licitations_table),7):
            edital = licitations_table[i+2].find_element(By.TAG_NAME, "a").get_attribute("href")
            licitation = {
                "central_de_compras": licitations_table[i].text,
                "processo": licitations_table[i+1].text,
                "edital": licitations_table[i+2].text,
                "data_publicacao": licitations_table[i+3].text,
                "modalidade": licitations_table[i+4].text,
                "objeto": licitations_table[i+5].text,
                "abertura_sessao": licitations_table[i+6].text,
                "lotes": get_lots(browser, edital)
            }
            licitations.append(licitation)
            save_data_json(licitation)
        try:
            next_page = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@class='next']/a[@href='#' and @title='Próximo']/i[@class='fa fa-angle-right']"))
            )
            next_page.click()
        except:
            print("No more pages")
            break
        
    return licitations

def get_lots(browser, edital):
    browser.execute_script("window.open('');")
    browser.switch_to.window(browser.window_handles[1])
    browser.get(edital)
    try:
        i = 1
        lots = []
        lots_len = len(WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//table[@id='lotsTable']/tbody/tr[@role='row']"))
        ))
        for i in range(1, lots_len + 1):
            cookies(browser)
            lotes_button = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//ul[@class='nav']/li/a[@href='#lotsTab']"))
            )
            lotes_button.click()
            lot = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//table[@id='lotsTable']/tbody/tr[@role='row'][{i}]"))
            )
            ActionChains(browser).move_to_element(lot).click().perform()
            lot = get_lot_info(browser)
            lots.append(lot)
            back_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@id='LtLink_voltar' and @class='btn']"))
            )
            back_button.click()
            i += 1
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        return lots
    except:
        print("No lot found: ", edital)
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        return lots

def get_lot_info(browser):
    try:
        description = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='identification']//tr[4]/td"))
        ).text
        proposals_start = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='disputeData']//tr[2]/td"))
        ).text
        proposals_end = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='disputeData']//tr[3]/td"))
        ).text
        products_len = len(WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//table[@id='itemsTable']/tbody/tr"))
        ))
        products = []
        for i in range(1, products_len + 1):
            product_name = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//table[@id='itemsTable']/tbody/tr[{i}]/td[3]"))
            ).text
            quantity = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//table[@id='itemsTable']/tbody/tr[{i}]/td[4]"))
            ).text
            unit = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//table[@id='itemsTable']/tbody/tr[{i}]/td[5]"))
            ).text
            code = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//table[@id='itemsTable']/tbody/tr[{i}]/td[2]"))
            ).text
            product = {
                "product_name": product_name,
                "code": code,
                "quantity": quantity,
                "unit": unit
            }
            products.append(product)
        lot = {
            "description": description,
            "proposals_start": proposals_start,
            "proposals_end": proposals_end,
            "products": products
        }
        return lot
    except:
        print("No lot info")

def save_data_json(licitation):
    output = 'data/licitacoes.json'
    os.makedirs(os.path.dirname(output), exist_ok=True)
    if os.path.exists(output) and os.path.getsize(output) > 0:
        with open(output, "r+", encoding="utf-8") as json_file:
            try:
                data = json.load(json_file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(licitation)
    with open(output, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

def save_data_csv(licitations):
    output = 'data/licitacoes.csv'
    os.makedirs(os.path.dirname(output), exist_ok=True)
    existing_data = []
    if os.path.exists(output) and os.path.getsize(output) > 0:
        with open(output, "r", encoding="utf-8", newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            existing_data = list(reader)
    
    if isinstance(licitations, list):
        existing_data.extend(licitations)
    else:
        existing_data.append(licitations)
    
    with open(output, "w", encoding="utf-8", newline='') as csv_file:
        if existing_data:
            fieldnames = existing_data[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(existing_data)
        print("Data saved")

def main():
    browser = navigator_initializer()
    licitations = collect_data(browser)

if __name__ == '__main__':
    main()