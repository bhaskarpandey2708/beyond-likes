# name: discourse-beyond-likes
# about: Prosocial discourse scoring and normative in-composer guidance for Discourse forums
# version: 1.0.0
# authors: Beyond Likes Team
# url: https://github.com/beyond-likes/discourse-plugin

enabled_site_setting :beyond_likes_enabled

after_initialize do
  on(:post_created) do |post, opts, user|
    return unless SiteSetting.beyond_likes_enabled

    # Call Beyond Likes Webhook
    begin
      uri = URI.parse(SiteSetting.beyond_likes_api_url || "http://localhost:8888/v1/webhooks/discourse")
      http = Net::HTTP.new(uri.host, uri.port)
      req = Net::HTTP::Post.new(uri.path, {'Content-Type' => 'application/json'})
      req.body = { post: { id: post.id, raw: post.raw, username: user.username, topic_id: post.topic_id } }.to_json
      
      response = http.request(req)
      result = JSON.parse(response.body)

      # If flagged uncivil or spam, automatically hide and queue for review
      if result["action"] == "quarantine_and_nudge"
        PostActionCreator.hide(post, PostActionType.types[:spam])
      elsif result["action"] == "pin_or_promote"
        # Optional: Add custom badge / prosocial tag
        post.custom_fields["beyond_likes_promoted"] = true
        post.save_custom_fields
      end
    rescue => e
      Rails.logger.warn("Beyond Likes Discourse error: #{e.message}")
    end
  end
end
