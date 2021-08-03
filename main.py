import flask
import pybadges
import api, logos

app = flask.Flask(__name__)

@app.route('/<site>/<user>')
def go(site, user):
	rating, rating_color = api.get_rating(site, user)
	badge = pybadges.badge(left_text=site, right_text=rating,
			left_color='black', right_color=rating_color, logo=logos.logos[site])
	badge = flask.make_response(badge)
	badge.content_type = 'image/svg+xml'
	return badge

if __name__ == '__main__':
	app.run(debug=False)

