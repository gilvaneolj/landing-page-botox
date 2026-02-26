<?php
// Facebook Conversions API (CAPI) Handler
// Handles "PageView" event server-side

$pixels = [
    [
        'id' => '2056520708244599',
        'token' => 'EAATDZBBlSuA0BQnixGEHq4qZBS5SZA9kw1tXOPw8ZCdxZALVH6765eNGIjyOmev4Fr8vUF0LmzZCrCzV3lto8ZBjOtr44DbjCxLdpoBbCg7vj2uefuBZAz73Xlb1VghjdWZB0QOp9ZAMUfB5gSQpzqv8ZC4RrzVU0s0dqGlpIJUkCUD2MF5LqKtOjZCUynNnprQ8JQZDZD'
    ],
    [
        'id' => '1415154023383690',
        'token' => 'EAAQf9PRghggBQ5iQjl6ZCO2dBf3RrOHjJLflGgJMS1F4v0wJ6PoExZCYvMGrTpswnOt0a7FZAvpVbm03LeIHW08QhdhMq4qS9itaES6hpOR5QiS11JKyV6unIh6R4VBDlcaqBMqNdEluMCaxmgDKq2b6LC4p9oaxogJAutWe6UlJZBwyyy9fKVZCgZBJmcYgZDZD'
    ]
];

// Get User Data
$client_ip = $_SERVER['REMOTE_ADDR'];
$client_user_agent = $_SERVER['HTTP_USER_AGENT'];
$fbp = isset($_COOKIE['_fbp']) ? $_COOKIE['_fbp'] : null;
$fbc = isset($_COOKIE['_fbc']) ? $_COOKIE['_fbc'] : null;

// Event Data Template
$event_data = [
    'data' => [
        [
            'event_name' => 'PageView',
            'event_time' => time(),
            'event_source_url' => (isset($_SERVER['HTTPS']) ? "https" : "http") . "://$_SERVER[HTTP_HOST]" . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH),
            'action_source' => 'website',
            'user_data' => [
                'client_ip_address' => $client_ip,
                'client_user_agent' => $client_user_agent,
                'fbp' => $fbp,
                'fbc' => $fbc
            ]
        ]
    ]
];

$responses = [];

foreach ($pixels as $pixel) {
    // Send to Facebook
    $url = "https://graph.facebook.com/v19.0/{$pixel['id']}/events?access_token={$pixel['token']}";

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($event_data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $responses[$pixel['id']] = json_decode(curl_exec($ch));
    curl_close($ch);
}

// Return generic success (silent)
header('Content-Type: application/json');
echo json_encode(['status' => 'sent', 'responses' => $responses]);
?>
