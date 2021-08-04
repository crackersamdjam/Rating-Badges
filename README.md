# Badges

Generates badges for users of progrmming sites with ratings and their corresponding colours.

Badges available at https://rating-badges.herokuapp.com/site/username where `site` is one of `Atcoder`, `Codeforces`, or `DMOJ`.

| Badge | URL |
|-|-|
| ![badge](https://rating-badges.herokuapp.com/Atcoder/crackersamdjam) | https://rating-badges.herokuapp.com/Atcoder/crackersamdjam |
| ![badge](https://rating-badges.herokuapp.com/Codeforces/crackersamdjam) | https://rating-badges.herokuapp.com/Codeforces/crackersamdjam |
| ![badge](https://rating-badges.herokuapp.com/DMOJ/crackersamdjam) | https://rating-badges.herokuapp.com/DMOJ/crackersamdjam |

Badges get cached and kept for a certain amount of time (currently 1 hour) to reduce the number of API queries. This is especially useful for Codeforces since the site goes down a lot.

Things to do:
- Display atcoder logo differently?
- What to do when cf is down? (which happens a lot)
- Logging
