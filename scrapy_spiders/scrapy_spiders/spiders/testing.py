def get_text_long(tag, *titles):
    bullet_list = []
    for title in titles:
        xpath = f'//title[contains(translate(. ,"ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{title}")]'
        section = response.xpath(f'{xpath}/parent::{tag}')

        # if section with specific title matches
        if section != []:
            # if section contains bullet points
            if section.xpath('./list') != []:
                for txt in response.xpath(f'{xpath}/parent::{tag}/descendant::p'):
                    bullet_point = txt.xpath('normalize-space()').get()
                    bullet_list.append(bullet_point)
                edited_text = '\n'.join(bullet_list)
                return edited_text
            else:
                str_title = response.xpath(f'normalize-space({xpath})').get()
                text = section.xpath('normalize-space()').get()
                edited_text  = re.sub(str_title, "", text).strip()
                return edited_text





    #
    #     # if section with the title from the argument exists continue processing
    #     if section != []:
    #         if section
    #
    #     #if section includes bullet points, for clarity output each line in newline
    #     if section.xpath('./list') != []:
    #         for txt in response.xpath(f'{xpath}/parent::{tag}/descendant::p'):
    #             bullet_point = txt.xpath('normalize-space()').get()
    #             bullet_list.append(bullet_point)
    #         edited_text = '\n'.join(bullet_list)
    #     # if section is not bullet-pointed output as normal text
    #     else:
    #         str_title = response.xpath(f'normalize-space({xpath})').get()
    #         text = section.xpath('normalize-space()').get()
    #         print(text)
    #     if text != None:
    #         # print(text)
    #         # if after passing all conditions text appears make final edit
    #         edited_text  = re.sub(str_title, "", text).strip()
    #         break
    #
    # return "NA" if not edited_text else edited_text
