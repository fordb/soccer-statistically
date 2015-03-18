import scrapy
import urlparse
from mls_shots.items import GameShotsItem


class ShotSpider(scrapy.Spider):
    name="shots"
    allowed_domains = ["matchcenter.mlssoccer.com"]
    start_urls = ["http://www.mlssoccer.com/schedule?month=3&year=2014&club=all&competition_type=46&broadcast_type=all&op=Search&form_id=mls_schedule_form"]
#                  "http://www.mlssoccer.com/schedule?month=4&year=2014&club=all&competition_type=46&broadcast_type=all&op=Search&form_id=mls_schedule_form",
#                  "http://www.mlssoccer.com/schedule?month=5&year=2014&club=all&competition_type=46&broadcast_type=all&op=Search&form_id=mls_schedule_form",
#                  "http://www.mlssoccer.com/schedule?month=6&year=2014&club=all&competition_type=46&broadcast_type=all&op=Search&form_id=mls_schedule_form",
#                  "http://www.mlssoccer.com/schedule?month=7&year=2014&club=all&competition_type=46&broadcast_type=all&op=Search&form_id=mls_schedule_form",
#                  "http://www.mlssoccer.com/schedule?month=8&year=2014&club=all&competition_type=46&broadcast_type=all&op=Search&form_id=mls_schedule_form",
#                  "http://www.mlssoccer.com/schedule?month=9&year=2014&club=all&competition_type=46&broadcast_type=all&op=Search&form_id=mls_schedule_form",
#                  "http://www.mlssoccer.com/schedule?month=10&year=2014&club=all&competition_type=46&broadcast_type=all&op=Search&form_id=mls_schedule_form"]

    def parse(self, response):
        links =  [l + "/stats" for l in response.xpath('//td[@class="views-field links"]//@href').extract() if 'matchcenter' in l]
        for l in links:
            yield scrapy.http.Request(l, callback=self.parse_game)


    def parse_game(self, response):
        game_id = 0
        game = GameShotsItem()
        home = response.xpath('//div[@class="sb-team sb-home"]/div[@class="sb-club-name"]/span[@class="sb-club-name-full"]//text()').extract()[0]
        away = response.xpath('//div[@class="sb-team sb-away"]/div[@class="sb-club-name"]/span[@class="sb-club-name-full"]//text()').extract()[0]
        shots = [s for s in response.xpath('//svg[@class="sa-shot-box"]/g//@data-reactid').extract()]
        for s in shots:
            try:
                x1 = float(response.xpath('//svg[@class="sa-shot-box"]/g[@data-reactid="{s}"]/line[@class="sa-shot-border"]//@x1'.format(s=s)).extract()[0].replace("%", ""))
                x2 = float(response.xpath('//svg[@class="sa-shot-box"]/g[@data-reactid="{s}"]/line[@class="sa-shot-border"]//@x2'.format(s=s)).extract()[0].replace("%", ""))
                y1 = float(response.xpath('//svg[@class="sa-shot-box"]/g[@data-reactid="{s}"]/line[@class="sa-shot-border"]//@y1'.format(s=s)).extract()[0].replace("%", ""))
                y2 = float(response.xpath('//svg[@class="sa-shot-box"]/g[@data-reactid="{s}"]/line[@class="sa-shot-border"]//@x1'.format(s=s)).extract()[0].replace("%", ""))
                if len(response.xpath('//svg[@class="sa-shot-box"]/g[@data-reactid="{s}"]/line//@class'.format(s=s)).extract()) > 0:
                    shot_type = response.xpath('//svg[@class="sa-shot-box"]/g[@data-reactid="{s}"]/line//@class'.format(s=s)).extract()[1]
                    try:
                        goal = response.xpath('//svg[@class="sa-shot-box"]/g[@data-reactid="{s}"]/circle//@class'.format(s=s)).extract()[0]
                    except IndexError:
                        goal = 'None'

                if "sa-shot-blocked" in shot_type:
                    outcome = 'blocked'
                elif goal == "None":
                    outcome = 'off target'
                elif "on-target" in goal:
                    outcome = 'on target'
                elif "goal" in goal:
                    outcome = 'goal'
                else:
                    outcome = '????'
                team = "???"
                                        
                game["x1"] = x1
                game["x2"] = x2
                game["y1"] = y1
                game["y2"] = y2
                game["outcome"] = outcome
                game["team"] = team
                game["id"] = game_id
            
            except IndexError:
                pass
            yield game
            game_id += 1
