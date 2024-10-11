int speed_id = 589;
int speed_pos = 3;
struct canfd_frame frame;

while (PollEvent(&event) != 0) {
    read_data(&event, &frame);
    if (frame.can_id == speed_id) {
        double speed = frame->data[speed_pos] << 8;
        speed += frame->data[speed_pos + 1];
        speed = speed / 100;
        speed = speed * 0.6213751;
        update_speed(speed);
    }
}