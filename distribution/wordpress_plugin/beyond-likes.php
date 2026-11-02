<?php
/**
 * Plugin Name: Normative Intelligence Discourse Intelligence
 * Plugin URI: https://beyondlikes.io
 * Description: Replaces legacy Perspective API with prosocial normative discourse scoring and constructive feedback.
 * Version: 1.0.0
 * Author: Normative Intelligence Team
 * License: GPLv2 or later
 */

if (!defined('ABSPATH')) exit;

add_filter('pre_comment_approved', 'beyond_likes_filter_comment', 10, 2);

function beyond_likes_filter_comment($approved, $commentdata) {
    $api_url = get_option('beyond_likes_endpoint', 'http://localhost:8888/v1/webhooks/wordpress');
    
    $payload = array(
        'comment_content' => $commentdata['comment_content'],
        'comment_author' => $commentdata['comment_author'],
        'comment_author_email' => $commentdata['comment_author_email']
    );

    $response = wp_remote_post($api_url, array(
        'method' => 'POST',
        'timeout' => 3,
        'headers' => array('Content-Type' => 'application/json'),
        'body' => json_encode($payload)
    ));

    if (is_wp_error($response)) {
        return $approved; // Fallback to default behavior if offline
    }

    $body = json_decode(wp_remote_retrieve_body($response), true);
    if (!empty($body['recommended_wp_status'])) {
        return $body['recommended_wp_status'];
    }

    return $approved;
}
