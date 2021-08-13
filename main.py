import flask
import pybadges
import api, logos

app = flask.Flask(__name__)

@app.route('/<site>/<user>')
def go(site, user):
	try:
		rating, rating_color = api.get_rating(site.lower(), user)
		badge = pybadges.badge(left_text=site, right_text=rating,
			left_color='black', right_color=rating_color, logo=logos.logos[site.lower()])
		badge = flask.make_response(badge)
		badge.content_type = 'image/svg+xml'
		return badge
	except:
		return 'Not Found', 400

@app.route('/')
def demo():
	base_url = flask.request.base_url
	examples = [(f'{base_url}Atcoder/crackersamdjam'),
				(f'{base_url}Codeforces/crackersamdjam'),
				(f'{base_url}DMOJ/crackersamdjam')]
	return flask.render_template('index.html', examples=examples)

if __name__ == '__main__':
	app.run(debug=False)

