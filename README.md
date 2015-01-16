team-news
=========

Python scripts to collect sport news for a team. It uses Newspaper (https://github.com/codelucas/newspaper/) to extract the news fields, and BeautifulSoup4 for missing fields such as author and published date.

Requirements:
=============
beautifulsoup4 (4.3.2)
newspaper==0.0.9.1

Examples:
=========

from team-news import getESPN_dot_com_team_news, getNBA_dot_com_team_news

news = getESPN_dot_com_team_news("Heat")

--output--
title: Miami Heat vs. Golden State Warriors  
link: http://scores.espn.go.com/nba/recap?gameId=400578874  
description: NBA Basketball Recap: Final statistics from the Miami Heat vs. Golden State Warriors game played on January 14, 2015  
text: OAKLAND, Calif. -- Golden State Warriors coach Steve Kerr has nothing but "good problems" right now...
image: http://a.espncdn.com/media/motion/2015/0114/dm_150114_nba_thtv_4v/dm_150114_nba_thtv_4v.jpg 
keywords: ['nba basketball Recap', 'Miami stats', 'Golden State stats']
author: Associated Press 
date: 2015-01-14T22:30:00-05:00 

title: Dwyane Wade of Miami Heat strains hamstring, is day to day 
link: http://espn.go.com/nba/story/_/id/12165076/dwyane-wade-miami-heat-strains-hamstring-day-day 
description: Miami Heat guard Dwyane Wade is likely to miss Wednesday's game against Golden State after leaving Tuesday's win over the Lakers with a strained hamstring. 
text: LOS ANGELES -- Miami Heat guard Dwyane Wade is likely to miss Wednesday's game against Golden State after leaving Tuesday's win over the Lakers with a strained hamstring...
keywords: ['dwyane wade', 'nba', 'nba', 'miami heat', 'hamstring', 'hammy', 'injury', 'hurt']
author: 
By 
Michael Wallace | ESPN.com 
date: 2015-01-14T22:43:00-05:00

...
----------


news = getNBA_dot_com_team_news("Heat")

--output--
title: HEAT Named NBA’s 2014 Retailer of The Year 
link: http://www.nba.com/heat/news/heat-named-nbas-2014-retailer-year 
description: MIAMI, FL – The Miami HEAT has been named the 2014 Team Retailer of the Year by the National Basketball Association for their successful merchandise sales during the 2013-14 NBA season. The HEAT is now the only five-time winner of the award, which has been given annually since 2002 to highlight the accomplishments of team merchandise sales and operations. 
text: MIAMI, FL – The Miami HEAT has been named the 2014 Team Retailer of the Year by the National Basketball Association for their successful merchandise sales during the 2013-14 NBA season. The HEAT is now the only five-time winner of the award, which has been given annually since 2002 to highlight the accomplishments of team merchandise sales and operations. The award recognizes the NBA’s most successful merchandising...
image: http://i.cdn.turner.com/drp/nba/heat/sites/default/files/780_2014retaileroftheyear-heatstore-02.jpg 
keywords: ['']
author: nba.com 
date: 2015-01-14T20:16:17-05:00

title: The Battier Take Charge Foundation Presents The Fourth Annual “South Beach Battioke” 
link: http://www.nba.com/heat/news/battier-take-charge-foundation-presents-fourth-annual-south-beach-battioke 
description: Miami, FL – Former Miami HEAT player, Shane Battier and his wife Heidi, continue to give back to the community they call home by hosting the fourth annual “South Beach Battioke” on March 3rd, 8 p.m. at the Fillmore Theatre in Miami Beach – a star-studded, karaoke charity event where attendees include Miami’s elite, philanthropists and socialites while watching their favorite Miami HEAT stars live out their pop star fantasies, all for a great cause. 
text: Miami, FL – Former Miami HEAT player, Shane Battier and his wife Heidi, continue to give back to the community they call home by hosting the fourth annual “South Beach Battioke” on March 3rd, 8 p.m. at the Fillmore Theatre in Miami Beach – a star-studded, karaoke charity event where attendees include Miami’s elite, philanthropists and socialites while watching their favorite Miami HEAT stars live out their pop star fantasies, all for a great cause...
image: http://i.cdn.turner.com/drp/nba/heat/sites/default/files/780_battioke_battier_150113.jpg 
keywords: ['']
author: nba.com 
date: 2015-01-13T20:16:24-05:00 

...
----------

